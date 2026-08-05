#!/usr/bin/env python3
"""
Единственный сборщик данных Clavis.to. Заменяет удалённый scripts/collect.py.

ПОЧЕМУ УДАЛЁН collect.py
════════════════════════
collect.py делал те же самые HTTP-запросы (GET /v1/models + GET /catalog/model/{id})
и сохранял подмножество тех же полей в data/history.csv. Держать два скрипта,
делающих одинаковые запросы к API — двойная нагрузка и двойное время workflow.
collect_extended.py собирает всё то же самое плюс новые поля нового формата API,
поэтому collect.py стал полностью избыточен и удалён.

КАК ОБЪЕДИНИТЬ СТАРУЮ ИСТОРИЮ (data/history.csv) С НОВОЙ (data/extended_history.csv)
══════════════════════════════════════════════════════════════════════════════════════
Если в репозитории уже накоплен data/history.csv с историей за несколько дней/недель,
эти данные не теряются — их можно влить в extended_history.csv одной командой:

    python scripts/migrate_history.py

Скрипт migrate_history.py (лежит рядом) читает старый history.csv и дописывает
строки в extended_history.csv, проставляя None в колонки, которых раньше не было
(pricing, benchmarks, uptime и т.д.). Строки за даты, которые уже есть в
extended_history.csv, пропускаются — идемпотентность гарантирована.

После успешной миграции history.csv можно удалить или оставить как архив —
скрипты больше его не читают.

ЧТО СОБИРАЕТСЯ
══════════════
Для каждой уникальной base-модели: GET https://api.clavis.to/catalog/model/{id}

Агрегируется по всем вариантам:
  total_requests              — сумма (тот же показатель, что был в collect.py)
  requests_24h                — сумма запросов за последние 24 ч.
  avg_uptime_pct              — средний uptime % по вариантам

Из самого дешёвого non-reserve per-token варианта:
  cheapest_input_per_1m_rub   — цена ввода
  cheapest_output_per_1m_rub  — цена вывода

Из корневого объекта модели:
  context_window              — максимальный контекст
  supports_caching            — поддержка кэша
  variant_count               — количество вариантов

Из benchmarks.livebench:
  livebench_global            — итоговый балл
  livebench_math / coding / reasoning / language — по категориям

СОХРАНЯЕТ
═════════
  data/snapshots/extended_YYYY-MM-DD.csv  — срез за сегодня
  data/snapshots/errors_YYYY-MM-DD.csv    — ошибки и модели без данных
  data/extended_history.csv               — накопительная история (дополняется)
"""

import csv
import datetime
import os
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MODELS_LIST_URL = "https://api.clavis.to/v1/models"
MODEL_DETAIL_URL = "https://api.clavis.to/catalog/model/{id}"

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
SNAPSHOTS_DIR = os.path.join(DATA_DIR, "snapshots")
EXTENDED_HISTORY_CSV = os.path.join(DATA_DIR, "extended_history.csv")

TODAY = datetime.date.today().isoformat()
EXTENDED_SNAPSHOT_CSV = os.path.join(SNAPSHOTS_DIR, f"extended_{TODAY}.csv")
ERRORS_CSV = os.path.join(SNAPSHOTS_DIR, f"errors_{TODAY}.csv")

REQUEST_TIMEOUT = 15
PAUSE_BETWEEN_CALLS = 0.35
USER_AGENT = "clavis-rating-github-actions/1.0"

HISTORY_FIELDNAMES = [
    "date", "base_id", "display_name", "vendor",
    "total_requests", "requests_24h",
    "context_window", "supports_caching",
    "cheapest_input_per_1m_rub", "cheapest_output_per_1m_rub",
    "avg_uptime_pct", "variant_count",
    "livebench_global", "livebench_math", "livebench_coding",
    "livebench_reasoning", "livebench_language",
]

SNAPSHOT_FIELDNAMES = [f for f in HISTORY_FIELDNAMES if f != "date"]


def _assert_ascii_header(value: str, name: str):
    try:
        value.encode("latin-1")
    except UnicodeEncodeError as e:
        raise ValueError(f"{name} содержит не-ASCII символы: {value!r}") from e


def build_session() -> requests.Session:
    _assert_ascii_header(USER_AGENT, "USER_AGENT")
    session = requests.Session()
    session.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    retry = Retry(
        total=5, backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_base_model_ids(session: requests.Session) -> list[str]:
    resp = session.get(MODELS_LIST_URL, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("data", data if isinstance(data, list) else [])
    seen: set[str] = set()
    base_ids: list[str] = []
    for m in items:
        if not m.get("is_active", True):
            continue
        base_id = m["id"].split("@")[0]
        if base_id not in seen:
            seen.add(base_id)
            base_ids.append(base_id)
    return base_ids


def fetch_model_stats(session: requests.Session, model_id: str) -> dict:
    url = MODEL_DETAIL_URL.format(id=model_id)
    r = session.get(url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    d = r.json()

    variants = d.get("variants", [])

    total_requests = 0
    requests_24h = 0
    uptime_vals: list[float] = []
    has_data = False

    for v in variants:
        u = v.get("uptime") or {}
        req = u.get("total_requests")
        if req is not None:
            total_requests += req
            has_data = True
        r24 = u.get("requests_24h")
        if r24 is not None:
            requests_24h += r24
        up = u.get("uptime")
        if up is not None:
            uptime_vals.append(up)

    avg_uptime = round(sum(uptime_vals) / len(uptime_vals), 1) if uptime_vals else None

    cheapest_input = None
    cheapest_output = None
    for v in variants:
        if v.get("is_reserve"):
            continue
        if v.get("billing_type") != "per_token":
            continue
        p = v.get("pricing") or {}
        inp = p.get("input_per_1m_rub")
        out = p.get("output_per_1m_rub")
        if inp is not None and (cheapest_input is None or inp < cheapest_input):
            cheapest_input = inp
            cheapest_output = out

    benchmarks = d.get("benchmarks") or {}
    lb = benchmarks.get("livebench") or {}
    lb_cats = lb.get("categories") or {}

    return {
        "base_id": d.get("base_id", model_id),
        "display_name": d.get("display_name", model_id),
        "vendor": d.get("vendor"),
        "total_requests": total_requests if has_data else None,
        "requests_24h": requests_24h if has_data else None,
        "context_window": d.get("context_window"),
        "supports_caching": d.get("supports_caching"),
        "cheapest_input_per_1m_rub": cheapest_input,
        "cheapest_output_per_1m_rub": cheapest_output,
        "avg_uptime_pct": avg_uptime,
        "variant_count": d.get("variant_count", len(variants)),
        "livebench_global": lb.get("global"),
        "livebench_math": lb_cats.get("math"),
        "livebench_coding": lb_cats.get("coding"),
        "livebench_reasoning": lb_cats.get("reasoning"),
        "livebench_language": lb_cats.get("language"),
    }


def append_to_history(results: list[dict]):
    """Дописывает сегодняшние данные в extended_history.csv.
    Идемпотентно: если строки за TODAY уже есть — удаляем их и пишем свежие.
    """
    existing_rows: list[dict] = []
    if os.path.exists(EXTENDED_HISTORY_CSV):
        with open(EXTENDED_HISTORY_CSV, newline="", encoding="utf-8") as f:
            existing_rows = [row for row in csv.DictReader(f) if row["date"] != TODAY]

    with open(EXTENDED_HISTORY_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HISTORY_FIELDNAMES)
        writer.writeheader()
        for row in existing_rows:
            writer.writerow(row)
        for r in results:
            writer.writerow({"date": TODAY, **r})


def main():
    os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
    session = build_session()

    base_ids = get_base_model_ids(session)
    print(f"Найдено уникальных base-моделей: {len(base_ids)}")

    results: list[dict] = []
    errors: list[dict] = []

    for i, model_id in enumerate(base_ids, 1):
        try:
            stats = fetch_model_stats(session, model_id)
            results.append(stats)
            print(f"[{i}/{len(base_ids)}] {model_id:35s} -> req={stats['total_requests']} lb={stats['livebench_global']}")
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            print(f"[{i}/{len(base_ids)}] {model_id:35s} -> HTTP {status}: {e}")
            errors.append({"base_id": model_id, "reason": "request_failed", "status_code": status, "message": str(e)})
        except Exception as e:
            print(f"[{i}/{len(base_ids)}] {model_id:35s} -> error: {e}")
            errors.append({"base_id": model_id, "reason": "request_failed", "status_code": None, "message": str(e)})
        time.sleep(PAUSE_BETWEEN_CALLS)

    no_data = [r for r in results if r["total_requests"] is None]
    results.sort(key=lambda r: (r["total_requests"] is None, -(r["total_requests"] or 0)))

    with open(EXTENDED_SNAPSHOT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=SNAPSHOT_FIELDNAMES)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

    with open(ERRORS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["base_id", "reason", "status_code", "message"])
        writer.writeheader()
        for e in errors:
            writer.writerow(e)
        for r in no_data:
            writer.writerow({
                "base_id": r["base_id"], "reason": "no_usage_data",
                "status_code": None,
                "message": "запрос прошёл успешно, но ни у одного варианта нет total_requests",
            })

    append_to_history(results)

    print(f"\nГотово. Снапшот: {EXTENDED_SNAPSHOT_CSV}")
    print(f"Ошибки/нет данных ({len(errors) + len(no_data)} шт.): {ERRORS_CSV}")
    print(f"История обновлена: {EXTENDED_HISTORY_CSV}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Собирает рейтинг моделей Clavis.to по количеству запросов (последние 30 дней)
и сохраняет результат в data/.

Вызывается из GitHub Actions раз в день (см. .github/workflows/daily-rating.yml),
но точно так же работает и локально: python scripts/collect.py

Что делает:
1. GET https://api.clavis.to/v1/models — список всех моделей.
2. Для каждой уникальной base-модели: GET https://api.clavis.to/catalog/model/{id}
   и суммирует total_requests по всем её вариантам/провайдерам.
3. Сохраняет:
   - data/snapshots/YYYY-MM-DD.csv       — срез рейтинга за сегодня
   - data/snapshots/errors_YYYY-MM-DD.csv — модели, по которым не удалось
     получить данные (сбой запроса ИЛИ отсутствие статистики)
   - data/history.csv                     — накопительная история (дописывается,
     не перезаписывается), формат: date, base_id, display_name, vendor,
     total_requests. На этом файле строится и README, и любая аналитика
     динамики по дням.
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
HISTORY_CSV = os.path.join(DATA_DIR, "history.csv")

TODAY = datetime.date.today().isoformat()
SNAPSHOT_CSV = os.path.join(SNAPSHOTS_DIR, f"{TODAY}.csv")
ERRORS_CSV = os.path.join(SNAPSHOTS_DIR, f"errors_{TODAY}.csv")

REQUEST_TIMEOUT = 15
PAUSE_BETWEEN_CALLS = 0.35

USER_AGENT = "clavis-rating-github-actions/1.0" #  (+https://github.com/nltagent/clavis_models_rating)


def build_session() -> requests.Session:
    session = requests.Session()
    session.headers.update({
        "User-Agent": USER_AGENT,
        "Accept": "application/json",
    })
    retry = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        respect_retry_after_header=True,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def get_base_model_ids(session: requests.Session):
    resp = session.get(MODELS_LIST_URL, timeout=REQUEST_TIMEOUT)
    resp.raise_for_status()
    data = resp.json()
    items = data.get("data", data if isinstance(data, list) else [])

    seen = set()
    base_ids = []
    for m in items:
        if not m.get("is_active", True):
            continue
        base_id = m["id"].split("@")[0]
        if base_id not in seen:
            seen.add(base_id)
            base_ids.append(base_id)
    return base_ids


def fetch_model_stats(session: requests.Session, model_id: str):
    url = MODEL_DETAIL_URL.format(id=model_id)
    r = session.get(url, timeout=REQUEST_TIMEOUT)
    r.raise_for_status()
    data = r.json()

    variants = data.get("variants", [])
    total = 0
    has_any_data = False
    for v in variants:
        uptime = v.get("uptime") or {}
        req = uptime.get("total_requests")
        if req is not None:
            total += req
            has_any_data = True

    return {
        "base_id": data.get("base_id", model_id),
        "display_name": data.get("display_name", model_id),
        "vendor": data.get("vendor"),
        "total_requests": total if has_any_data else None,
        "variant_count": data.get("variant_count", len(variants)),
    }


def append_to_history(results):
    is_new_file = not os.path.exists(HISTORY_CSV)
    with open(HISTORY_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "base_id", "display_name", "vendor", "total_requests"])
        if is_new_file:
            writer.writeheader()
        for r in results:
            writer.writerow({
                "date": TODAY,
                "base_id": r["base_id"],
                "display_name": r["display_name"],
                "vendor": r["vendor"],
                "total_requests": r["total_requests"],
            })


def main():
    os.makedirs(SNAPSHOTS_DIR, exist_ok=True)
    session = build_session()

    base_ids = get_base_model_ids(session)
    print(f"Найдено уникальных base-моделей: {len(base_ids)}")

    results = []
    errors = []
    for i, model_id in enumerate(base_ids, 1):
        try:
            stats = fetch_model_stats(session, model_id)
            results.append(stats)
            print(f"[{i}/{len(base_ids)}] {model_id:35s} -> {stats['total_requests']}")
        except requests.HTTPError as e:
            status = e.response.status_code if e.response is not None else None
            print(f"[{i}/{len(base_ids)}] {model_id:35s} -> HTTP error: {e}")
            errors.append({"base_id": model_id, "reason": "request_failed", "status_code": status, "message": str(e)})
        except Exception as e:
            print(f"[{i}/{len(base_ids)}] {model_id:35s} -> error: {e}")
            errors.append({"base_id": model_id, "reason": "request_failed", "status_code": None, "message": str(e)})
        time.sleep(PAUSE_BETWEEN_CALLS)

    no_data = [r for r in results if r["total_requests"] is None]
    results.sort(key=lambda r: (r["total_requests"] is None, -(r["total_requests"] or 0)))

    with open(SNAPSHOT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["base_id", "display_name", "vendor", "total_requests", "variant_count"])
        writer.writeheader()
        for r in results:
            writer.writerow({
                "base_id": r["base_id"],
                "display_name": r["display_name"],
                "vendor": r["vendor"],
                "total_requests": r["total_requests"],
                "variant_count": r["variant_count"],
            })

    with open(ERRORS_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["base_id", "reason", "status_code", "message"])
        writer.writeheader()
        for e in errors:
            writer.writerow(e)
        for r in no_data:
            writer.writerow({
                "base_id": r["base_id"],
                "reason": "no_usage_data",
                "status_code": None,
                "message": "запрос прошёл успешно, но ни у одного варианта нет total_requests",
            })

    append_to_history(results)

    print(f"\nГотово. Снапшот: {SNAPSHOT_CSV}")
    print(f"Ошибки/нет данных ({len(errors) + len(no_data)} шт.): {ERRORS_CSV}")
    print(f"История обновлена: {HISTORY_CSV}")


if __name__ == "__main__":
    main()

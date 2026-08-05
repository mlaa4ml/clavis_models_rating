#!/usr/bin/env python3
"""
Генерирует docs/index.html — GitHub Pages страницу с несколькими рейтингами:

  1. 🔥 По популярности (total_requests, 30 дн.) — базовый рейтинг
  2. ⚡ Активность за 24 часа (requests_24h)
  3. 🧠 По качеству (LiveBench global score)
  4. 💰 По дешевизне (cheapest input price, руб./1M токенов)
  5. 📐 По размеру контекста
  6. 🔄 По стабильности (средний uptime %)

Читает data/extended_history.csv (свежайшую дату).
Публикуется в docs/index.html — GitHub Pages branch docs/.
"""

import csv
import datetime
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
EXTENDED_HISTORY_CSV = os.path.join(DATA_DIR, "extended_history.csv")
DOCS_DIR = os.path.join(REPO_ROOT, "docs")
OUTPUT_HTML = os.path.join(DOCS_DIR, "index.html")

TOP_N = 20


def load_latest() -> list[dict]:
    if not os.path.exists(EXTENDED_HISTORY_CSV):
        return []
    by_date: dict[str, dict] = {}
    with open(EXTENDED_HISTORY_CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d = row["date"]
            by_date.setdefault(d, {})[row["base_id"]] = row
    if not by_date:
        return []
    latest = sorted(by_date.keys())[-1]
    rows = list(by_date[latest].values())

    def to_num(v, typ=float):
        try:
            return typ(v) if v not in (None, "", "None") else None
        except (ValueError, TypeError):
            return None

    for r in rows:
        r["total_requests"]             = to_num(r.get("total_requests"), int)
        r["requests_24h"]               = to_num(r.get("requests_24h"), int)
        r["context_window"]             = to_num(r.get("context_window"), int)
        r["avg_uptime_pct"]             = to_num(r.get("avg_uptime_pct"))
        r["cheapest_input_per_1m_rub"]  = to_num(r.get("cheapest_input_per_1m_rub"))
        r["cheapest_output_per_1m_rub"] = to_num(r.get("cheapest_output_per_1m_rub"))
        r["livebench_global"]           = to_num(r.get("livebench_global"))
        r["livebench_math"]             = to_num(r.get("livebench_math"))
        r["livebench_coding"]           = to_num(r.get("livebench_coding"))
        r["livebench_reasoning"]        = to_num(r.get("livebench_reasoning"))
        r["livebench_language"]         = to_num(r.get("livebench_language"))
        r["supports_caching"]           = str(r.get("supports_caching", "")).lower() in ("true", "1", "yes")
    return rows


def fmt_num(v, decimals=0):
    if v is None:
        return "<span class='na'>—</span>"
    if decimals == 0:
        return f"{int(v):,}".replace(",", "\u202f")
    return f"{v:,.{decimals}f}".replace(",", "\u202f")


def fmt_ctx(v):
    if v is None:
        return "<span class='na'>—</span>"
    if v >= 1_000_000:
        return f"{v/1_000_000:.1f}M"
    if v >= 1_000:
        return f"{v//1_000}K"
    return str(v)


def medal(rank: int) -> str:
    return ["🥇", "🥈", "🥉"][rank] if rank < 3 else str(rank + 1)


def vendor_badge(vendor: str | None) -> str:
    if not vendor:
        return ""
    colors = {
        "Google": "#4285F4", "Anthropic": "#c96442", "OpenAI": "#10a37f",
        "Meta": "#0866FF", "Mistral": "#ff7000", "DeepSeek": "#4361EE",
        "xAI": "#000000", "Cohere": "#39594d",
    }
    color = colors.get(vendor, "#6b7280")
    return f'<span class="badge" style="background:{color}">{vendor}</span>'


def build_table(rows: list[dict], sort_key: str, ascending=False,
                columns: list[tuple] | None = None,
                filter_fn=None) -> str:
    """
    columns: list of (header, render_fn) tuples
    render_fn receives the row dict.
    """
    filtered = [r for r in rows if r.get(sort_key) is not None]
    if filter_fn:
        filtered = [r for r in filtered if filter_fn(r)]
    filtered.sort(key=lambda r: r[sort_key], reverse=not ascending)
    filtered = filtered[:TOP_N]

    if not filtered:
        return "<p class='empty'>Данные ещё не собраны.</p>"

    headers = ["#", "Модель", "Провайдер"] + [c[0] for c in (columns or [])]
    th = "".join(f"<th>{h}</th>" for h in headers)
    rows_html = []
    for i, r in enumerate(filtered):
        name = r.get("display_name") or r.get("base_id", "?")
        cells = [
            f"<td class='rank'>{medal(i)}</td>",
            f"<td class='model-name'>{name}</td>",
            f"<td>{vendor_badge(r.get('vendor'))}</td>",
        ]
        for _, fn in (columns or []):
            cells.append(f"<td>{fn(r)}</td>")
        cls = "top3" if i < 3 else ""
        rows_html.append(f"<tr class='{cls}'>{''.join(cells)}</tr>")

    return f"""<table>
<thead><tr>{th}</tr></thead>
<tbody>{''.join(rows_html)}</tbody>
</table>"""


def build_html(rows: list[dict], generated_at: str) -> str:
    # ---------- Rating 1: Popularity ----------
    r1 = build_table(rows, "total_requests", columns=[
        ("Запросов (30 дн.)", lambda r: fmt_num(r["total_requests"])),
        ("За 24 ч.",          lambda r: fmt_num(r["requests_24h"])),
        ("Вариантов",         lambda r: r.get("variant_count", "—")),
    ])

    # ---------- Rating 2: Activity 24h ----------
    r2 = build_table(rows, "requests_24h", columns=[
        ("За 24 ч.",          lambda r: fmt_num(r["requests_24h"])),
        ("За 30 дн.",         lambda r: fmt_num(r["total_requests"])),
    ])

    # ---------- Rating 3: LiveBench quality ----------
    r3 = build_table(rows, "livebench_global", columns=[
        ("LiveBench",  lambda r: f"<strong>{r['livebench_global']}</strong>" if r.get("livebench_global") else "<span class='na'>—</span>"),
        ("Math",       lambda r: fmt_num(r.get("livebench_math"))),
        ("Coding",     lambda r: fmt_num(r.get("livebench_coding"))),
        ("Reasoning",  lambda r: fmt_num(r.get("livebench_reasoning"))),
        ("Language",   lambda r: fmt_num(r.get("livebench_language"))),
    ])

    # ---------- Rating 4: Cheapest models ----------
    r4 = build_table(rows, "cheapest_input_per_1m_rub", ascending=True,
        filter_fn=lambda r: r.get("cheapest_input_per_1m_rub") is not None,
        columns=[
            ("Ввод ₽/1M",  lambda r: fmt_num(r["cheapest_input_per_1m_rub"], 2) + " ₽"),
            ("Вывод ₽/1M", lambda r: fmt_num(r.get("cheapest_output_per_1m_rub"), 2) + " ₽"),
            ("Кэш",        lambda r: "✅" if r.get("supports_caching") else "—"),
        ]
    )

    # ---------- Rating 5: Context window ----------
    r5 = build_table(rows, "context_window", columns=[
        ("Контекст",   lambda r: fmt_ctx(r["context_window"])),
        ("Кэш",        lambda r: "✅" if r.get("supports_caching") else "—"),
    ])

    # ---------- Rating 6: Uptime stability ----------
    r6 = build_table(rows, "avg_uptime_pct", columns=[
        ("Uptime %",   lambda r: f"{r['avg_uptime_pct']:.1f}%"),
        ("Запросов",   lambda r: fmt_num(r["total_requests"])),
    ])

    return f"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Clavis.to — Рейтинги моделей</title>
<style>
  :root {{
    --bg: #0f1117; --surface: #1a1d27; --border: #2a2d3e;
    --text: #e2e8f0; --muted: #94a3b8; --accent: #7c6af7;
    --gold: #f59e0b; --silver: #94a3b8; --bronze: #b45309;
    --green: #10b981; --red: #ef4444;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: system-ui, -apple-system, sans-serif; padding: 24px; }}
  h1 {{ font-size: 1.6rem; font-weight: 700; margin-bottom: 4px; }}
  .subtitle {{ color: var(--muted); font-size: 0.875rem; margin-bottom: 32px; }}
  .subtitle a {{ color: var(--accent); text-decoration: none; }}
  .grid {{ display: grid; gap: 32px; }}
  .card {{ background: var(--surface); border: 1px solid var(--border); border-radius: 12px; padding: 20px; }}
  .card h2 {{ font-size: 1.05rem; font-weight: 600; margin-bottom: 16px; display: flex; align-items: center; gap: 8px; }}
  .card h2 .desc {{ font-weight: 400; color: var(--muted); font-size: 0.8rem; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 0.85rem; }}
  th {{ text-align: left; padding: 8px 10px; color: var(--muted); font-weight: 500; border-bottom: 1px solid var(--border); white-space: nowrap; }}
  td {{ padding: 8px 10px; border-bottom: 1px solid var(--border); vertical-align: middle; }}
  tr:last-child td {{ border-bottom: none; }}
  tr.top3 td {{ background: rgba(124,106,247,0.04); }}
  td.rank {{ font-weight: 700; font-size: 1rem; width: 40px; }}
  td.model-name {{ font-weight: 500; max-width: 240px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }}
  .badge {{ display: inline-block; padding: 2px 7px; border-radius: 20px; font-size: 0.7rem; font-weight: 600; color: #fff; white-space: nowrap; }}
  .na {{ color: var(--muted); }}
  .empty {{ color: var(--muted); padding: 16px 0; }}
  footer {{ margin-top: 40px; color: var(--muted); font-size: 0.8rem; text-align: center; }}
  @media (min-width: 900px) {{
    .grid {{ grid-template-columns: 1fr 1fr; }}
    .wide {{ grid-column: 1 / -1; }}
  }}
</style>
</head>
<body>

<h1>Clavis.to — Рейтинги моделей</h1>
<p class="subtitle">
  Авто-обновление раз в день · Источник: <a href="https://clavis.to/models" target="_blank">clavis.to</a>
  · Обновлено: {generated_at} UTC
</p>

<div class="grid">

  <div class="card wide">
    <h2>🔥 Популярность <span class="desc">суммарных запросов за 30 дней</span></h2>
    {r1}
  </div>

  <div class="card">
    <h2>⚡ Активность за 24 ч <span class="desc">горячий тренд</span></h2>
    {r2}
  </div>

  <div class="card">
    <h2>🔄 Стабильность <span class="desc">средний uptime по вариантам</span></h2>
    {r6}
  </div>

  <div class="card wide">
    <h2>🧠 Качество <span class="desc">LiveBench global score</span></h2>
    {r3}
  </div>

  <div class="card">
    <h2>💰 Дешевизна <span class="desc">ввод ₽ за 1M токенов, меньше = лучше</span></h2>
    {r4}
  </div>

  <div class="card">
    <h2>📐 Размер контекста <span class="desc">максимальный контекст</span></h2>
    {r5}
  </div>

</div>

<footer>
  Данные: <a href="https://api.clavis.to" style="color:var(--accent)">api.clavis.to</a> ·
  Бенчмарки: <a href="https://livebench.ai" style="color:var(--accent)">LiveBench</a> (Apache-2.0) ·
  Код: <a href="https://github.com/" style="color:var(--accent)">GitHub</a>
</footer>

</body>
</html>"""


def main():
    os.makedirs(DOCS_DIR, exist_ok=True)
    rows = load_latest()
    now = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M")
    html = build_html(rows, now)
    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[build_ratings_page] Страница сохранена: {OUTPUT_HTML}")
    if not rows:
        print("[build_ratings_page] ВНИМАНИЕ: данные не найдены, запусти collect_extended.py сначала.")


if __name__ == "__main__":
    main()

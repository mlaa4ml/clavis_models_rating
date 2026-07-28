#!/usr/bin/env python3
"""
Генерирует таблицу рейтинга (топ-N моделей по запросам за 30 дней, с дельтой
к предыдущему дню) и вставляет её в README.md между маркерами:

    <!-- RATING_TABLE_START -->
    ... (сюда подставляется таблица) ...
    <!-- RATING_TABLE_END -->

Запускается после collect.py в том же workflow-запуске, читает уже
обновлённый data/history.csv.
"""

import csv
import datetime
import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")
HISTORY_CSV = os.path.join(DATA_DIR, "history.csv")
README_PATH = os.path.join(REPO_ROOT, "README.md")

START_MARKER = "<!-- RATING_TABLE_START -->"
END_MARKER = "<!-- RATING_TABLE_END -->"

TOP_N = 25


def load_history():
    """Читаем всю историю, группируем по датам."""
    by_date = {}  # date -> {base_id: row}
    if not os.path.exists(HISTORY_CSV):
        return by_date

    with open(HISTORY_CSV, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = row["date"]
            by_date.setdefault(date, {})
            total = row["total_requests"]
            row["total_requests"] = int(total) if total not in (None, "", "None") else None
            by_date[date][row["base_id"]] = row
    return by_date


def build_table(by_date):
    if not by_date:
        return "_Данные ещё не собраны._"

    dates_sorted = sorted(by_date.keys())
    latest_date = dates_sorted[-1]
    prev_date = dates_sorted[-2] if len(dates_sorted) >= 2 else None

    latest = by_date[latest_date]
    prev = by_date.get(prev_date, {})

    rows = list(latest.values())
    rows.sort(key=lambda r: (r["total_requests"] is None, -(r["total_requests"] or 0)))

    lines = []
    lines.append(f"_Обновлено: {latest_date} (UTC) · моделей в рейтинге: {len(rows)}_")
    lines.append("")
    lines.append("| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |")
    lines.append("|---|--------|-----------|-------------------:|--------------:|")

    for i, r in enumerate(rows[:TOP_N], 1):
        name = r["display_name"] or r["base_id"]
        vendor = r["vendor"] or "—"
        total = r["total_requests"]
        total_str = f"{total:,}".replace(",", " ") if total is not None else "—"

        prev_row = prev.get(r["base_id"])
        delta_str = "—"
        if total is not None and prev_row and prev_row["total_requests"] is not None:
            delta = total - prev_row["total_requests"]
            if delta > 0:
                delta_str = f"🔺 +{delta:,}".replace(",", " ")
            elif delta < 0:
                delta_str = f"🔻 {delta:,}".replace(",", " ")
            else:
                delta_str = "0"

        lines.append(f"| {i} | {name} | {vendor} | {total_str} | {delta_str} |")

    return "\n".join(lines)


def update_readme(table_markdown: str):
    if not os.path.exists(README_PATH):
        raise FileNotFoundError(f"README.md не найден по пути {README_PATH}")

    with open(README_PATH, encoding="utf-8") as f:
        content = f.read()

    if START_MARKER not in content or END_MARKER not in content:
        raise ValueError(
            f"В README.md не найдены маркеры {START_MARKER} / {END_MARKER}. "
            "Проверь, что они есть в файле дословно."
        )

    before = content.split(START_MARKER)[0]
    after = content.split(END_MARKER)[1]

    new_content = f"{before}{START_MARKER}\n{table_markdown}\n{END_MARKER}{after}"

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(new_content)


def main():
    by_date = load_history()
    table = build_table(by_date)
    update_readme(table)
    print("README.md обновлён.")


if __name__ == "__main__":
    main()

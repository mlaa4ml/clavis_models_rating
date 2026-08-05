#!/usr/bin/env python3
"""
Миграция старой data/history.csv → data/extended_history.csv.

КОГДА НУЖЕН ЭТОТ СКРИПТ
════════════════════════
Если до перехода на collect_extended.py в репозитории уже накопился
data/history.csv (старый формат: date, base_id, display_name, vendor,
total_requests) — этот скрипт переносит ту историю в новый файл
extended_history.csv, чтобы не потерять накопленную динамику.

Поля, которых не было в старом формате (pricing, benchmarks, uptime и т.д.),
заполняются пустым значением (None). В рейтингах по этим полям старые строки
просто не участвуют — это корректное поведение.

КАК ЗАПУСТИТЬ
═════════════
    python scripts/migrate_history.py

Скрипт идемпотентен: строки за даты, которые уже есть в extended_history.csv,
пропускаются. Можно запускать повторно без риска дублей.

После успешной миграции убедись, что в extended_history.csv появились нужные
даты, и при желании удали старый history.csv:

    # Проверить что перенеслось:
    python -c "
    import csv
    dates = sorted({r['date'] for r in csv.DictReader(open('data/extended_history.csv'))})
    print(f'{len(dates)} дат, первая: {dates[0]}, последняя: {dates[-1]}')
    "

    # Удалить старый файл (необязательно, скрипты его больше не читают):
    rm data/history.csv
    git rm data/history.csv
    git commit -m "chore: remove legacy history.csv after migration to extended_history.csv"

ЕСЛИ history.csv НЕТ
════════════════════
Скрипт завершается с сообщением и кодом 0 — это не ошибка, просто нечего мигрировать.
"""

import csv
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(REPO_ROOT, "data")

OLD_CSV = os.path.join(DATA_DIR, "history.csv")
NEW_CSV = os.path.join(DATA_DIR, "extended_history.csv")

NEW_FIELDNAMES = [
    "date", "base_id", "display_name", "vendor",
    "total_requests", "requests_24h",
    "context_window", "supports_caching",
    "cheapest_input_per_1m_rub", "cheapest_output_per_1m_rub",
    "avg_uptime_pct", "variant_count",
    "livebench_global", "livebench_math", "livebench_coding",
    "livebench_reasoning", "livebench_language",
]

# Поля, которые есть в старом формате (подмножество NEW_FIELDNAMES)
OLD_FIELDNAMES = {"date", "base_id", "display_name", "vendor", "total_requests"}


def main():
    if not os.path.exists(OLD_CSV):
        print(f"data/history.csv не найден — нечего мигрировать.")
        print("Это нормально, если проект запускается впервые после перехода.")
        sys.exit(0)

    # Читаем старую историю
    old_rows: list[dict] = []
    with open(OLD_CSV, newline="", encoding="utf-8") as f:
        old_rows = list(csv.DictReader(f))
    print(f"Прочитано строк из history.csv: {len(old_rows)}")

    # Читаем уже существующие даты в новом файле (если файл есть)
    existing_dates: set[str] = set()
    existing_rows: list[dict] = []
    if os.path.exists(NEW_CSV):
        with open(NEW_CSV, newline="", encoding="utf-8") as f:
            existing_rows = list(csv.DictReader(f))
        existing_dates = {r["date"] for r in existing_rows}
        print(f"В extended_history.csv уже есть данные за {len(existing_dates)} дат: "
              f"{sorted(existing_dates)[:3]}{'...' if len(existing_dates) > 3 else ''}")

    # Фильтруем старые строки — берём только даты, которых нет в новом файле
    to_migrate = [r for r in old_rows if r["date"] not in existing_dates]
    skipped = len(old_rows) - len(to_migrate)

    if not to_migrate:
        print("Все даты из history.csv уже есть в extended_history.csv — ничего не делаю.")
        sys.exit(0)

    print(f"Будет перенесено: {len(to_migrate)} строк "
          f"(пропущено как уже существующие: {skipped})")

    # Пишем объединённый файл: сначала старые мигрируемые строки, потом существующие новые
    # (сортировка по дате обеспечит правильный порядок)
    migrated_rows = []
    for r in to_migrate:
        new_row = {f: "" for f in NEW_FIELDNAMES}
        for field in OLD_FIELDNAMES:
            new_row[field] = r.get(field, "")
        migrated_rows.append(new_row)

    all_rows = migrated_rows + existing_rows
    all_rows.sort(key=lambda r: r["date"])

    with open(NEW_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=NEW_FIELDNAMES)
        writer.writeheader()
        for row in all_rows:
            writer.writerow(row)

    dates_migrated = sorted({r["date"] for r in migrated_rows})
    print(f"\nГотово. Перенесено дат: {len(dates_migrated)}")
    print(f"  Первая: {dates_migrated[0]}")
    print(f"  Последняя: {dates_migrated[-1]}")
    print(f"  Итого строк в extended_history.csv: {len(all_rows)}")
    print(f"\nСтарый файл data/history.csv НЕ удалён — удали вручную, когда убедишься")
    print(f"что данные перенеслись корректно (см. инструкцию в шапке этого скрипта).")


if __name__ == "__main__":
    main()

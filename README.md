# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://YOUR_USERNAME.github.io/clavis-rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-05 (UTC) · моделей в рейтинге: 189_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gemini-3.1-pro-preview | Google | 4 735 | 🔺 +196 |
| 2 | gpt-5.6-sol | OpenAI | 4 392 | 0 |
| 3 | deepseek-v4-pro | DeepSeek | 2 161 | 🔺 +12 |
| 4 | gpt-5.6-luna | OpenAI | 2 120 | 🔺 +16 |
| 5 | claude-sonnet-4-6 | Anthropic | 1 688 | 0 |
| 6 | deepseek-v4-flash | DeepSeek | 1 509 | 🔺 +5 |
| 7 | gemini-3-flash-preview | Google | 1 503 | 🔺 +3 |
| 8 | gpt-5.5 | OpenAI | 1 465 | 🔺 +284 |
| 9 | claude-opus-4-8 | Anthropic | 1 141 | 0 |
| 10 | claude-opus-4-7 | Anthropic | 987 | 0 |
| 11 | gpt-5-mini | OpenAI | 974 | 0 |
| 12 | gpt-5.4-mini | OpenAI | 972 | 🔺 +13 |
| 13 | gpt-5.6-terra | OpenAI | 814 | 🔺 +455 |
| 14 | gemini-3.1-flash-lite | Google | 752 | 0 |
| 15 | claude-opus-5 | Anthropic | 736 | 0 |
| 16 | gpt-5-nano | OpenAI | 681 | 🔺 +2 |
| 17 | gemini-3.6-flash | Google | 613 | 🔺 +4 |
| 18 | gpt-5.4 | OpenAI | 526 | 0 |
| 19 | claude-sonnet-5 | Anthropic | 509 | 0 |
| 20 | gemini-3.5-flash | Google | 296 | 0 |
| 21 | gemini-2.5-pro | Google | 239 | 0 |
| 22 | text-embedding-3-small | OpenAI | 215 | 🔺 +12 |
| 23 | claude-fable-5 | Anthropic | 178 | 0 |
| 24 | Aion 3.0 | Aion Labs | 171 | 🔺 +4 |
| 25 | gemini-embedding-001 | Google | 114 | 🔺 +1 |
<!-- RATING_TABLE_END -->

## Расширенные рейтинги (GitHub Pages)

Страница `docs/index.html` содержит **6 рейтингов**:

| | Рейтинг | Метрика |
|---|---------|---------|
| 🔥 | Популярность | `total_requests` за 30 дней |
| ⚡ | Активность | `requests_24h` — горячий тренд |
| 🧠 | Качество | LiveBench global score |
| 💰 | Дешевизна | минимальная цена ввода ₽/1M токенов |
| 📐 | Контекст | максимальный `context_window` |
| 🔄 | Стабильность | средний uptime по вариантам |

## Как это работает

```
collect_extended.py  ──→  extended_history.csv
                                  │
                    ┌─────────────┴──────────────┐
                    ▼                            ▼
           update_readme.py           build_ratings_page.py
           (README.md)                (docs/index.html)
```

1. `scripts/collect_extended.py` — единственный сборщик. Делает запросы к API
   и сохраняет полный набор полей: запросы, цены, контекст, uptime, бенчмарки.
2. `scripts/update_readme.py` — читает `extended_history.csv`, строит таблицу топ-25 с дельтой.
3. `scripts/build_ratings_page.py` — генерирует `docs/index.html` (GitHub Pages).
4. Workflow коммитит `data/*`, `README.md`, `docs/` раз в день.

## Данные

| Файл | Описание |
|------|----------|
| `data/extended_history.csv` | Полная история со всеми полями (основной файл) |
| `data/snapshots/extended_YYYY-MM-DD.csv` | Снапшот за день |
| `data/snapshots/errors_YYYY-MM-DD.csv` | Ошибки сбора |

## Миграция старой истории

Если в репозитории накопился старый `data/history.csv` (формат до объединения
сборщиков) — его данные можно перенести без потерь:

```bash
python scripts/migrate_history.py
```

Скрипт дописывает старые строки в `extended_history.csv`, заполняя новые поля
пустыми значениями. Идемпотентен — безопасно запускать повторно.

## Локальный запуск

```bash
pip install -r requirements.txt

python scripts/collect_extended.py   # сбор данных
python scripts/update_readme.py      # обновить README
python scripts/build_ratings_page.py # собрать HTML → docs/index.html
```

## Настройка GitHub Pages

**Settings → Pages → Source: Deploy from branch → Branch: `main`, Folder: `/docs`**

## Расписание

По умолчанию — 06:00 UTC. Менять в `.github/workflows/daily-rating.yml`, поле `cron`.

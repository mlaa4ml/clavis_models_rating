# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-30 (UTC) · моделей в рейтинге: 132_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | Claude Opus 5 | Anthropic | 36 760 | 🔺 +20 696 |
| 2 | GPT-5.6 Luna | OpenAI | 5 262 | — |
| 3 | Gemini 3.1 Flash Lite | Google | 5 185 | 🔺 +4 080 |
| 4 | GPT-5.6 Terra | OpenAI | 2 306 | 🔺 +90 |
| 5 | Gemini 3.1 Pro Preview | Google | 2 288 | 🔺 +136 |
| 6 | GPT-5.6 Sol | OpenAI | 1 889 | — |
| 7 | Claude Opus 4.7 | Anthropic | 1 424 | 🔺 +41 |
| 8 | Gemini 3 Flash Preview | Google | 886 | 🔺 +4 |
| 9 | text-embedding-3-small@Azure | OpenAI | 755 | 🔺 +9 |
| 10 | GPT-4o-mini | OpenAI | 726 | 🔺 +11 |
| 11 | Hy3 | Tencent | 694 | 🔺 +150 |
| 12 | Gemini 3.7 Flash | Google | 560 | 🔺 +12 |
| 13 | Gemini 3.6 Flash | Google | 491 | 🔺 +262 |
| 14 | GLM 5.1 | Zhipu | 376 | 🔺 +127 |
| 15 | GPT-5.4 Mini | OpenAI | 346 | 0 |
| 16 | Claude Sonnet 5 | Anthropic | 247 | 🔺 +184 |
| 17 | GPT-5.5 | OpenAI | 231 | 🔺 +40 |
| 18 | GLM 5.3 | Zhipu | 223 | 🔺 +112 |
| 19 | DeepSeek V4 Flash 0731 | DeepSeek | 201 | 🔺 +26 |
| 20 | GPT-4o | OpenAI | 188 | 🔺 +58 |
| 21 | Claude Opus 4.8 | Anthropic | 131 | 🔺 +9 |
| 22 | Gemini 2.5 Flash | Google | 100 | 🔺 +1 |
| 23 | DeepSeek V4 Pro 0813 | DeepSeek | 98 | 🔺 +82 |
| 24 | GLM 5.3 Flash | Zhipu | 97 | 🔺 +29 |
| 25 | Claude Sonnet 4.6 | Anthropic | 91 | 🔻 -1 |
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

По умолчанию — 07:22 UTC. Менять в `.github/workflows/daily-rating.yml`, поле `cron`.

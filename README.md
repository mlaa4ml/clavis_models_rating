# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-06 (UTC) · моделей в рейтинге: 129_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | Claude Opus 5 | Anthropic | 182 599 | 🔺 +1 482 |
| 2 | GPT-5.6 Luna | OpenAI | 9 516 | 🔺 +1 004 |
| 3 | Gemini 3.1 Flash Lite | Google | 7 321 | 0 |
| 4 | GPT-4.1 Mini | OpenAI | 4 630 | 🔺 +74 |
| 5 | Hy3 | Tencent | 3 403 | 🔺 +601 |
| 6 | GPT-5.6 Terra | OpenAI | 3 384 | 🔺 +490 |
| 7 | Gemini 3.1 Pro Preview | Google | 2 866 | 🔺 +178 |
| 8 | GPT-5.6 Sol | OpenAI | 2 200 | 🔺 +79 |
| 9 | Claude Opus 4.7 | Anthropic | 1 170 | 0 |
| 10 | text-embedding-3-small | OpenAI | 927 | 🔺 +31 |
| 11 | GLM 5.3 | Zhipu | 789 | 🔺 +253 |
| 12 | GPT-4o-mini | OpenAI | 740 | 0 |
| 13 | GLM 5.3 Flash | Zhipu | 703 | 🔺 +609 |
| 14 | Gemini 3.7 Flash | Google | 648 | 🔺 +24 |
| 15 | GLM 5.1 | Zhipu | 605 | 0 |
| 16 | Gemini 3.6 Flash | Google | 462 | 🔻 -10 |
| 17 | Claude Sonnet 5 | Anthropic | 449 | 🔺 +9 |
| 18 | Claude Opus 4.8 | Anthropic | 396 | 🔺 +9 |
| 19 | GPT-5.4 Mini | OpenAI | 379 | 0 |
| 20 | Gemini 3.8 Flash | Google | 305 | 🔺 +123 |
| 21 | Kimi K3 | Moonshot | 235 | 🔺 +4 |
| 22 | GPT-5.5 | OpenAI | 230 | 0 |
| 23 | GPT-4o | OpenAI | 218 | 0 |
| 24 | GLM 5.3 | Zhipu | 161 | 🔺 +62 |
| 25 | Grok 4.5 | xAI | 145 | 🔺 +15 |
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

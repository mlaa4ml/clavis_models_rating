# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-25 (UTC) · моделей в рейтинге: 133_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | GPT-5.6 Luna | OpenAI | 16 425 | 🔻 -88 |
| 2 | Hy3 | Tencent | 12 061 | 0 |
| 3 | GPT-4.1 Mini | OpenAI | 11 609 | 🔺 +761 |
| 4 | Gemini 3.1 Flash Lite | Google | 8 267 | 0 |
| 5 | Gemini 3.1 Pro Preview | Google | 6 486 | 🔻 -87 |
| 6 | Claude Opus 4.8 | Anthropic | 6 342 | 🔺 +1 908 |
| 7 | GPT-5.6 Terra | OpenAI | 5 529 | 🔻 -129 |
| 8 | Gemini 3.8 Flash | Google | 4 700 | 🔺 +69 |
| 9 | GPT-5.6 Sol | OpenAI | 3 348 | 🔻 -142 |
| 10 | Gemini 3.7 Flash | Google | 2 431 | 🔻 -37 |
| 11 | text-embedding-3-small@Azure | OpenAI | 2 307 | 🔻 -3 |
| 12 | Claude Opus 5 | Anthropic | 2 011 | 🔺 +39 |
| 13 | GPT-6 Astra | OpenAI | 1 906 | 🔺 +96 |
| 14 | GPT-5.5 | OpenAI | 1 880 | 🔻 -20 |
| 15 | GLM 5.3 Flash | Zhipu | 1 851 | 🔺 +17 |
| 16 | Claude Sonnet 5 | Anthropic | 1 016 | 🔺 +18 |
| 17 | GPT-4o-mini | OpenAI | 777 | 🔺 +13 |
| 18 | GLM 5.3 | Zhipu | 692 | 🔺 +1 |
| 19 | GPT-5 Mini | OpenAI | 671 | 🔺 +50 |
| 20 | Gemini 3.6 Flash | Google | 610 | 🔺 +29 |
| 21 | DeepSeek V4 Pro 0813 | DeepSeek | 478 | 🔻 -1 |
| 22 | Claude Sonnet 4.6 | Anthropic | 477 | 🔺 +1 |
| 23 | GPT-5.4 Mini | OpenAI | 331 | 0 |
| 24 | Kimi K3 | Moonshot | 311 | 🔺 +3 |
| 25 | GPT-4o | OpenAI | 262 | 0 |
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

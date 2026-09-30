# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-30 (UTC) · моделей в рейтинге: 146_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | Claude Opus 4.8 | Anthropic | 15 409 | 🔺 +28 |
| 2 | GPT-5.6 Luna | OpenAI | 13 094 | 🔻 -1 019 |
| 3 | Hy3 | Tencent | 11 081 | 🔻 -324 |
| 4 | GPT-4.1 Mini | OpenAI | 9 467 | 🔻 -3 752 |
| 5 | GPT-4o-mini | OpenAI | 8 420 | 🔺 +4 029 |
| 6 | Gemini 3.1 Pro Preview | Google | 6 146 | 🔻 -138 |
| 7 | Gemini 3.8 Flash | Google | 4 993 | 🔺 +13 |
| 8 | GPT-5.6 Terra | OpenAI | 4 852 | 🔻 -45 |
| 9 | GPT-5.6 Sol | OpenAI | 3 950 | 🔺 +134 |
| 10 | Gemini 3.7 Flash | Google | 2 456 | 🔺 +11 |
| 11 | text-embedding-3-small@Azure | OpenAI | 2 296 | 🔻 -2 |
| 12 | Claude Opus 5 | Anthropic | 2 256 | 🔺 +13 |
| 13 | Gemini 3.1 Flash Lite | Google | 2 204 | 🔻 -775 |
| 14 | GLM 5.3 Flash | Zhipu | 2 075 | 🔺 +60 |
| 15 | GPT-6 Astra | OpenAI | 2 010 | 🔺 +28 |
| 16 | GPT-5.5 | OpenAI | 1 906 | 0 |
| 17 | Claude Sonnet 5 | Anthropic | 959 | 🔺 +62 |
| 18 | Claude Haiku 4.5 | Anthropic | 854 | 0 |
| 19 | GPT-5 Mini | OpenAI | 836 | 🔺 +122 |
| 20 | DeepSeek V4 Pro 0813 | DeepSeek | 779 | 🔺 +15 |
| 21 | GLM 5.3 | Zhipu | 735 | 0 |
| 22 | Claude Sonnet 4.6 | Anthropic | 513 | 0 |
| 23 | Gemini 3.6 Flash | Google | 423 | 🔻 -13 |
| 24 | GPT-5.4 Mini | OpenAI | 345 | 🔺 +4 |
| 25 | Kimi K3 | Moonshot | 333 | 🔺 +8 |
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

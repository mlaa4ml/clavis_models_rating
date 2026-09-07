# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-07 (UTC) · моделей в рейтинге: 128_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | GPT-5.6 Luna | OpenAI | 9 908 | 🔺 +392 |
| 2 | Gemini 3.1 Flash Lite | Google | 7 465 | 🔺 +144 |
| 3 | GPT-4.1 Mini | OpenAI | 4 804 | 🔺 +174 |
| 4 | GPT-5.6 Terra | OpenAI | 3 980 | 🔺 +596 |
| 5 | Hy3 | Tencent | 3 509 | 🔺 +106 |
| 6 | Gemini 3.1 Pro Preview | Google | 3 138 | 🔺 +272 |
| 7 | text-embedding-3-small | OpenAI | 2 472 | 🔺 +1 545 |
| 8 | GPT-5.6 Sol | OpenAI | 2 265 | 🔺 +65 |
| 9 | Claude Opus 4.7 | Anthropic | 1 164 | 🔻 -6 |
| 10 | GLM 5.3 Flash | Zhipu | 975 | 🔺 +272 |
| 11 | GLM 5.3 | Zhipu | 880 | 🔺 +91 |
| 12 | Claude Opus 5 | Anthropic | 848 | 🔻 -181 751 |
| 13 | GPT-4o-mini | OpenAI | 742 | 🔺 +2 |
| 14 | Gemini 3.7 Flash | Google | 657 | 🔺 +9 |
| 15 | GLM 5.1 | Zhipu | 607 | 🔺 +2 |
| 16 | Claude Sonnet 5 | Anthropic | 487 | 🔺 +38 |
| 17 | Gemini 3.6 Flash | Google | 469 | 🔺 +7 |
| 18 | GPT-5.4 Mini | OpenAI | 408 | 🔺 +29 |
| 19 | Gemini 3.8 Flash | Google | 305 | 0 |
| 20 | Kimi K3 | Moonshot | 235 | 0 |
| 21 | GPT-5.5 | OpenAI | 231 | 🔺 +1 |
| 22 | GPT-4o | OpenAI | 220 | 🔺 +2 |
| 23 | Claude Opus 4.8 | Anthropic | 178 | 🔻 -218 |
| 24 | GLM 5.3 | Zhipu | 167 | 🔺 +6 |
| 25 | Claude Sonnet 4.6 | Anthropic | 152 | 🔺 +7 |
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

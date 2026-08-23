# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-23 (UTC) · моделей в рейтинге: 185_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | DeepSeek V4 Flash 0731 | DeepSeek | 6 547 | 🔺 +611 |
| 2 | Claude Opus 4.7 | Anthropic | 1 633 | 0 |
| 3 | Gemini 3.1 Pro Preview | Google | 1 613 | 🔺 +304 |
| 4 | GPT-5.6 Luna | OpenAI | 1 240 | 🔺 +318 |
| 5 | Claude Opus 5 | Anthropic | 1 214 | 🔺 +189 |
| 6 | Qwen3.7 Flash | Alibaba | 1 133 | 🔺 +508 |
| 7 | Gemini 3 Flash Preview | Google | 878 | 0 |
| 8 | GPT-5.6 Terra | OpenAI | 728 | 🔺 +125 |
| 9 | GPT-5.6 Sol | OpenAI | 680 | 🔺 +158 |
| 10 | text-embedding-3-small@Azure | OpenAI | 538 | 🔺 +464 |
| 11 | Gemini 3.7 Flash | Google | 351 | 🔺 +294 |
| 12 | DeepSeek V4 Flash 0731 | DeepSeek | 260 | 🔺 +48 |
| 13 | Claude Sonnet 4.6 | Anthropic | 134 | 🔺 +3 |
| 14 | DeepSeek V3.2 | DeepSeek | 122 | 0 |
| 15 | Gemini 3.6 Flash | Google | 115 | 🔺 +18 |
| 16 | GPT-5.5 | OpenAI | 106 | 🔺 +65 |
| 17 | Grok 4.6 | xAI | 94 | 🔺 +34 |
| 18 | GPT-5.4 Mini | OpenAI | 88 | 🔻 -177 |
| 19 | GPT-5.4 | OpenAI | 80 | 🔺 +56 |
| 20 | DeepSeek V4 Pro 0813 | DeepSeek | 77 | 🔺 +4 |
| 21 | Gemini 2.5 Flash | Google | 68 | 🔺 +48 |
| 22 | Hy3 | Tencent | 63 | 0 |
| 23 | GLM 5.2 | Zhipu | 51 | 0 |
| 24 | Claude Sonnet 5 | Anthropic | 50 | 0 |
| 25 | Gemini 2.5 Pro | Google | 46 | 🔺 +5 |
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

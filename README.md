# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-20 (UTC) · моделей в рейтинге: 357_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | Gemini 3.1 Pro Preview | Google | 6 222 | 🔺 +129 |
| 2 | GPT-5.6 Luna | OpenAI | 6 210 | 🔺 +1 012 |
| 3 | DeepSeek V4 Flash 0731 | DeepSeek | 5 235 | 🔺 +221 |
| 4 | GPT-5.6 Terra | OpenAI | 2 368 | 🔺 +281 |
| 5 | GPT-5.5 | OpenAI | 2 241 | 🔻 -22 |
| 6 | DeepSeek V4 Pro 0813 | DeepSeek | 1 986 | 🔺 +7 |
| 7 | Claude Opus 4.7 | Anthropic | 1 940 | 🔺 +1 915 |
| 8 | Claude Opus 5 | Anthropic | 1 857 | 🔺 +1 447 |
| 9 | Claude Sonnet 4.6 | Anthropic | 1 750 | 🔺 +1 704 |
| 10 | Claude Sonnet 5 | Anthropic | 1 287 | 🔺 +115 |
| 11 | GPT-5.6 Sol | OpenAI | 1 201 | 🔻 -37 |
| 12 | Claude Opus 4.8 | Anthropic | 1 056 | 🔺 +143 |
| 13 | Gemini 3.6 Flash | Google | 976 | 🔺 +1 |
| 14 | Gemini 3 Flash Preview | Google | 884 | 0 |
| 15 | Gemini 3.1 Flash Lite | Google | 782 | 🔺 +116 |
| 16 | GPT-5.4 Mini | OpenAI | 772 | 🔻 -1 |
| 17 | GPT-5 Nano | OpenAI | 686 | 0 |
| 18 | GPT-5 Mini | OpenAI | 404 | 🔺 +6 |
| 19 | GPT-5.4 | OpenAI | 353 | 🔺 +4 |
| 20 | DeepSeek V4 Flash 0731 | DeepSeek | 343 | 🔻 -7 |
| 21 | Kimi K3 | Moonshot | 332 | 0 |
| 22 | GLM 5.2 | Zhipu | 315 | 0 |
| 23 | text-embedding-3-small | OpenAI | 235 | 🔺 +47 |
| 24 | Qwen3.7 Flash | Alibaba | 226 | 🔺 +7 |
| 25 | Grok 4.5 | xAI | 152 | 🔺 +52 |
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

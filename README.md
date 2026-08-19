# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-19 (UTC) · моделей в рейтинге: 360_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | Gemini 3.1 Pro Preview | Google | 6 093 | 🔺 +5 244 |
| 2 | GPT-5.6 Luna | OpenAI | 5 198 | 🔺 +5 185 |
| 3 | DeepSeek V4 Flash 0731 | DeepSeek | 5 014 | 🔺 +301 |
| 4 | GPT-5.5 | OpenAI | 2 263 | 🔺 +2 259 |
| 5 | GPT-5.6 Terra | OpenAI | 2 087 | 🔺 +2 086 |
| 6 | DeepSeek V4 Pro 0813 | DeepSeek | 1 979 | 🔺 +1 968 |
| 7 | GPT-5.6 Sol | OpenAI | 1 238 | 🔺 +1 226 |
| 8 | Claude Sonnet 5 | Anthropic | 1 172 | 🔺 +933 |
| 9 | Gemini 3.6 Flash | Google | 975 | 🔺 +973 |
| 10 | Claude Opus 4.8 | Anthropic | 913 | 🔺 +910 |
| 11 | Gemini 3 Flash Preview | Google | 884 | — |
| 12 | GPT-5.4 Mini | OpenAI | 773 | 🔺 +773 |
| 13 | GPT-5 Nano | OpenAI | 686 | 🔺 +686 |
| 14 | Gemini 3.1 Flash Lite | Google | 666 | 🔺 +666 |
| 15 | Claude Opus 5 | Anthropic | 410 | 🔺 +403 |
| 16 | GPT-5 Mini | OpenAI | 398 | 🔺 +396 |
| 17 | DeepSeek V4 Flash 0731 | DeepSeek | 350 | 🔺 +195 |
| 18 | GPT-5.4 | OpenAI | 349 | 🔺 +127 |
| 19 | Kimi K3 | Moonshot | 332 | 🔺 +318 |
| 20 | GLM 5.2 | Zhipu | 315 | 🔺 +270 |
| 21 | Qwen3.7 Flash | Alibaba | 219 | 🔺 +2 |
| 22 | text-embedding-3-small | OpenAI | 188 | — |
| 23 | Aion-3.0 | Aion Labs | 141 | 🔺 +1 |
| 24 | Claude Sonnet 4.6 | Anthropic | 141 | 🔺 +16 |
| 25 | Claude Fable 5 | Anthropic | 109 | 🔺 +105 |
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

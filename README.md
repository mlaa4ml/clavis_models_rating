# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-21 (UTC) · моделей в рейтинге: 190_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | DeepSeek V4 Flash 0731 | DeepSeek | 5 761 | 🔺 +526 |
| 2 | Claude Opus 4.7 | Anthropic | 1 633 | 🔻 -307 |
| 3 | Gemini 3.1 Pro Preview | Google | 1 269 | 🔻 -4 953 |
| 4 | Claude Opus 5 | Anthropic | 881 | 🔻 -976 |
| 5 | Gemini 3 Flash Preview | Google | 878 | 🔻 -6 |
| 6 | GPT-5.4 Mini | OpenAI | 379 | 🔻 -393 |
| 7 | Qwen3.7 Flash | Alibaba | 265 | 🔺 +39 |
| 8 | GPT-5.6 Sol | OpenAI | 225 | 🔻 -976 |
| 9 | DeepSeek V4 Flash 0731 | DeepSeek | 208 | 🔻 -135 |
| 10 | GPT-5.6 Terra | OpenAI | 172 | 🔻 -2 196 |
| 11 | GPT-5.6 Luna | OpenAI | 160 | 🔻 -6 050 |
| 12 | Claude Sonnet 4.6 | Anthropic | 120 | 🔻 -1 630 |
| 13 | Aion-3.0 | Aion Labs | 116 | 🔻 -9 |
| 14 | DeepSeek V3.2 | DeepSeek | 108 | 🔺 +96 |
| 15 | Gemini 3.6 Flash | Google | 82 | 🔻 -894 |
| 16 | DeepSeek V4 Pro 0813 | DeepSeek | 71 | 🔻 -1 915 |
| 17 | Hy3 | Tencent | 63 | 🔺 +3 |
| 18 | GLM 5.2 | Zhipu | 51 | 🔻 -264 |
| 19 | Claude Sonnet 5 | Anthropic | 47 | 🔻 -1 240 |
| 20 | Aion-2.0 | Aion Labs | 46 | 0 |
| 21 | Grok 4.6 | xAI | 46 | 🔺 +16 |
| 22 | Qwen3 Coder Plus | Alibaba | 38 | 🔺 +4 |
| 23 | GPT-5 Mini | OpenAI | 37 | 🔻 -367 |
| 24 | Claude Opus 4.8 | Anthropic | 34 | 🔻 -1 022 |
| 25 | Qwen3.8 Max | Alibaba | 34 | 🔻 -1 |
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

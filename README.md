# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-29 (UTC) · моделей в рейтинге: 128_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | Claude Opus 5 | Anthropic | 16 064 | 🔺 +7 037 |
| 2 | gpt-5.6-terra@CodexPro | OpenAI | 2 216 | 🔺 +230 |
| 3 | [req]gemini-3.1-pro-preview | Google | 2 152 | 🔻 -74 |
| 4 | claude-opus-4-7 | Anthropic | 1 383 | 0 |
| 5 | gemini-3.1-flash-lite@geminipro | Google | 1 105 | 🔺 +994 |
| 6 | gemini-3-flash-preview@geminipro | Google | 882 | 0 |
| 7 | text-embedding-3-small@Azure | OpenAI | 746 | 🔺 +2 |
| 8 | gpt-4o-mini | OpenAI | 715 | 🔺 +338 |
| 9 | [req]gemini-3.7-flash@request | Google | 548 | 🔺 +1 |
| 10 | Hy3 | Tencent | 544 | 🔺 +152 |
| 11 | gpt-5.4-mini@Azure | OpenAI | 346 | 0 |
| 12 | GLM 5.1 | Zhipu | 249 | 🔺 +245 |
| 13 | gemini-3.6-flash@geminipro | Google | 229 | 🔺 +29 |
| 14 | gpt-5.5@CodexPro | OpenAI | 191 | 0 |
| 15 | DeepSeek V4 Flash | DeepSeek | 175 | 0 |
| 16 | gpt-4o | OpenAI | 130 | 🔺 +123 |
| 17 | Claude Opus 4.8 | Anthropic | 122 | 🔺 +6 |
| 18 | glm-5.3@Temp | Zhipu | 111 | 0 |
| 19 | gemini-2.5-flash@gemini | Google | 99 | 0 |
| 20 | claude-sonnet-4-6@claudecode | Anthropic | 92 | 🔻 -18 |
| 21 | gpt-5.4@azureopenai | OpenAI | 88 | 0 |
| 22 | [req]glm-5.3-flash@request | Zhipu | 68 | 🔺 +68 |
| 23 | [req]claude-sonnet-5 | Anthropic | 63 | 0 |
| 24 | gemini-2.5-pro-r | Google | 57 | 0 |
| 25 | claude-fable-5 | Anthropic | 46 | 0 |
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

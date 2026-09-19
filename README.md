# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-19 (UTC) · моделей в рейтинге: 133_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gpt-5.6-luna@CodexPro | OpenAI | 15 411 | 🔺 +664 |
| 2 | Hy3 | Tencent | 12 064 | 🔻 -3 |
| 3 | gpt-4.1-mini | OpenAI | 9 036 | 🔺 +363 |
| 4 | gemini-3.1-flash-lite-r | Google | 7 947 | 🔻 -1 |
| 5 | gemini-3.1-pro-preview@request | Google | 6 594 | 🔺 +198 |
| 6 | gpt-5.6-terra@azureopenai | OpenAI | 6 354 | 🔺 +161 |
| 7 | [free]gpt-5.6-sol@request | OpenAI | 3 921 | 🔺 +121 |
| 8 | gemini-3.8-flash@gemini | Google | 3 527 | 🔺 +73 |
| 9 | text-embedding-3-small@Azure | OpenAI | 3 009 | 🔺 +1 |
| 10 | gpt-5.5@CodexPro | OpenAI | 1 896 | 🔺 +882 |
| 11 | claude-opus-5@ClaudeMix | Anthropic | 1 692 | 🔻 -134 |
| 12 | gpt-6-astra@codex | OpenAI | 1 626 | 🔺 +10 |
| 13 | [free]gemini-3.7-flash@request | Google | 1 354 | 🔺 +107 |
| 14 | [free]GLM-5.3-flash@request | Zhipu | 1 304 | 🔺 +86 |
| 15 | glm-5.3-flash@Temp | Zhipu | 1 280 | 🔺 +45 |
| 16 | [free]GLM-5.3@request | Zhipu | 983 | 🔺 +206 |
| 17 | claude-sonnet-5@ClaudeMix | Anthropic | 934 | 0 |
| 18 | gpt-4o-mini | OpenAI | 746 | 0 |
| 19 | claude-opus-4-8@ClaudeMix | Anthropic | 718 | 🔺 +2 |
| 20 | [free]deepseek-v4-pro-0813@request | DeepSeek | 679 | 🔺 +200 |
| 21 | gemini-3.6-flash@geminipro | Google | 559 | 🔺 +49 |
| 22 | claude-sonnet-4-6@ClaudeMix | Anthropic | 505 | 🔻 -1 |
| 23 | gpt-5-mini | OpenAI | 448 | 🔺 +108 |
| 24 | [req]deepseek-v4-pro | DeepSeek | 427 | 🔺 +1 |
| 25 | gpt-4o | OpenAI | 262 | 0 |
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

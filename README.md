# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-03 (UTC) · моделей в рейтинге: 131_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | [free]claude-opus-5@request | Anthropic | 124 700 | 🔺 +15 996 |
| 2 | GPT 5.6 Luna | OpenAI | 8 276 | 🔺 +216 |
| 3 | gemini-3.1-flash-lite@geminipro | Google | 7 321 | 0 |
| 4 | gpt-4.1-mini | OpenAI | 3 787 | 0 |
| 5 | gpt-5.6-terra | OpenAI | 2 620 | 🔺 +5 |
| 6 | [req]gemini-3.1-pro-preview | Google | 2 560 | 🔺 +14 |
| 7 | gpt-5.6-sol | OpenAI | 1 998 | 🔺 +4 |
| 8 | Hy3 | Tencent | 1 987 | 🔺 +133 |
| 9 | claude-opus-4-7@ClaudeLite | Anthropic | 1 225 | 🔺 +37 |
| 10 | text-embedding-3-small@Azure | OpenAI | 837 | 🔺 +5 |
| 11 | gpt-4o-mini | OpenAI | 733 | 🔺 +1 |
| 12 | gemini-3.7-flash-r | Google | 658 | 🔺 +16 |
| 13 | [req]glm-5.1 | Zhipu | 601 | 🔺 +13 |
| 14 | glm-5.3@Temp | Zhipu | 589 | 🔺 +111 |
| 15 | claude-sonnet-5 | Anthropic | 543 | 0 |
| 16 | Gemini 3.1 Flash Lite Preview | Google | 491 | 0 |
| 17 | gemini-3.6-flash@geminipro | Google | 488 | 0 |
| 18 | [free]deepseek-v4-pro-0813@request | DeepSeek | 373 | 0 |
| 19 | gpt-5.4-mini@CodexPro | OpenAI | 352 | 🔺 +5 |
| 20 | gpt-5.5@CodexPro | OpenAI | 339 | 🔺 +10 |
| 21 | claude-opus-4-8@ClaudeLite | Anthropic | 264 | 🔺 +11 |
| 22 | gpt-4o | OpenAI | 209 | 0 |
| 23 | [req]glm-5.3-flash@request | Zhipu | 165 | 🔺 +67 |
| 24 | grok-4.5@GrokBuild | xAI | 119 | 🔺 +2 |
| 25 | DeepSeek V4 Pro | DeepSeek | 110 | 🔺 +3 |
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

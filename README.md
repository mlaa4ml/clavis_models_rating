# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-07 (UTC) · моделей в рейтинге: 187_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gemini-3.1-pro-preview | Google | 4 892 | 🔺 +35 |
| 2 | gpt-5.6-sol | OpenAI | 4 417 | 0 |
| 3 | deepseek-v4-pro | DeepSeek | 2 169 | 🔻 -4 |
| 4 | gpt-5.6-luna | OpenAI | 2 138 | 🔺 +18 |
| 5 | gpt-5.5 | OpenAI | 1 720 | 🔺 +267 |
| 6 | claude-sonnet-4-6 | Anthropic | 1 683 | 🔻 -1 |
| 7 | deepseek-v4-flash | DeepSeek | 1 533 | 🔻 -9 |
| 8 | gemini-3-flash-preview | Google | 1 394 | 🔻 -35 |
| 9 | gpt-5.4-mini | OpenAI | 1 019 | 0 |
| 10 | gpt-5.6-terra | OpenAI | 1 009 | 🔺 +54 |
| 11 | claude-opus-4-7 | Anthropic | 987 | 0 |
| 12 | gpt-5-mini | OpenAI | 971 | 0 |
| 13 | gemini-3.1-flash-lite | Google | 751 | 0 |
| 14 | claude-opus-5 | Anthropic | 736 | 0 |
| 15 | gpt-5-nano | OpenAI | 682 | 🔺 +1 |
| 16 | gemini-3.6-flash | Google | 676 | 🔺 +54 |
| 17 | claude-sonnet-5 | Anthropic | 492 | 🔻 -17 |
| 18 | claude-opus-4-8 | Anthropic | 467 | 🔻 -174 |
| 19 | gpt-5.4 | OpenAI | 435 | 🔻 -29 |
| 20 | text-embedding-3-small | OpenAI | 387 | 🔺 +66 |
| 21 | GLM-5.2 | Zhipu | 296 | 🔺 +40 |
| 22 | gemini-3.5-flash | Google | 290 | 0 |
| 23 | kimi-k3 | Moonshot | 290 | 0 |
| 24 | gemini-2.5-pro | Google | 236 | 🔻 -2 |
| 25 | claude-fable-5 | Anthropic | 177 | 🔻 -1 |
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

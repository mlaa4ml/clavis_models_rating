# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-09 (UTC) · моделей в рейтинге: 193_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gemini-3.1-pro-preview | Google | 5 077 | 🔺 +158 |
| 2 | gpt-5.6-sol | OpenAI | 4 447 | 🔻 -12 |
| 3 | gpt-5.6-luna | OpenAI | 2 728 | 🔺 +144 |
| 4 | deepseek-v4-pro | DeepSeek | 2 217 | 🔺 +8 |
| 5 | claude-sonnet-4-6 | Anthropic | 1 679 | 🔻 -1 |
| 6 | gpt-5.5 | OpenAI | 1 646 | 🔺 +15 |
| 7 | deepseek-v4-flash | DeepSeek | 1 394 | 🔻 -139 |
| 8 | gpt-5.6-terra | OpenAI | 1 219 | 🔺 +210 |
| 9 | gemini-3-flash-preview | Google | 1 208 | 🔻 -79 |
| 10 | claude-opus-4-7 | Anthropic | 1 020 | 🔺 +26 |
| 11 | gpt-5-mini | OpenAI | 972 | 🔻 -14 |
| 12 | claude-sonnet-5 | Anthropic | 867 | 🔺 +351 |
| 13 | gpt-5.4-mini | OpenAI | 829 | 🔻 -45 |
| 14 | claude-opus-4-8 | Anthropic | 762 | 🔺 +266 |
| 15 | claude-opus-5 | Anthropic | 736 | 0 |
| 16 | gemini-3.6-flash | Google | 696 | 🔺 +7 |
| 17 | gpt-5-nano | OpenAI | 682 | 0 |
| 18 | gemini-3.1-flash-lite | Google | 623 | 0 |
| 19 | gpt-5.4 | OpenAI | 401 | 🔻 -12 |
| 20 | kimi-k3 | Moonshot | 336 | 0 |
| 21 | GLM-5.2 | Zhipu | 291 | 🔻 -2 |
| 22 | text-embedding-3-small | OpenAI | 291 | 🔻 -95 |
| 23 | gemini-3.5-flash | Google | 290 | 0 |
| 24 | Aion 3.0 | Aion Labs | 190 | 🔺 +18 |
| 25 | claude-fable-5 | Anthropic | 176 | 🔻 -1 |
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

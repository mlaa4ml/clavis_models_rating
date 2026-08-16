# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-16 (UTC) · моделей в рейтинге: 208_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gemini-3.1-pro-preview | Google | 5 836 | 🔺 +94 |
| 2 | gpt-5.6-luna | OpenAI | 4 067 | 🔺 +300 |
| 3 | gpt-5.5 | OpenAI | 2 301 | 🔻 -49 |
| 4 | deepseek-v4-pro | DeepSeek | 1 908 | 🔻 -95 |
| 5 | gpt-5.6-terra | OpenAI | 1 712 | 🔺 +37 |
| 6 | claude-sonnet-4-6 | Anthropic | 1 703 | 🔺 +22 |
| 7 | claude-opus-4-7 | Anthropic | 1 352 | 🔺 +385 |
| 8 | claude-opus-5 | Anthropic | 1 287 | 🔺 +77 |
| 9 | gpt-5.6-sol | OpenAI | 1 056 | 🔺 +13 |
| 10 | claude-sonnet-5 | Anthropic | 896 | 🔺 +21 |
| 11 | gemini-3-flash-preview | Google | 884 | 0 |
| 12 | claude-opus-4-8 | Anthropic | 846 | 🔺 +24 |
| 13 | gpt-5.4-mini | OpenAI | 747 | 🔺 +24 |
| 14 | gemini-3.6-flash | Google | 719 | 🔺 +3 |
| 15 | gpt-5-nano | OpenAI | 683 | 🔺 +1 |
| 16 | DeepSeek V4 Flash 0731 | DeepSeek | 650 | 🔺 +58 |
| 17 | gemini-3.1-flash-lite | Google | 631 | 🔺 +2 |
| 18 | gpt-5-mini | OpenAI | 607 | 🔻 -103 |
| 19 | gpt-5.4 | OpenAI | 584 | 🔺 +242 |
| 20 | kimi-k3 | Moonshot | 349 | 0 |
| 21 | deepseek-v4-flash | DeepSeek | 315 | 🔻 -94 |
| 22 | GLM-5.2 | Zhipu | 313 | 0 |
| 23 | text-embedding-3-small | OpenAI | 187 | 0 |
| 24 | Aion 3.0 | Aion Labs | 140 | 🔻 -13 |
| 25 | gemini-embedding-001 | Google | 105 | 🔻 -3 |
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

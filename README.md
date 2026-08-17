# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-17 (UTC) · моделей в рейтинге: 336_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gemini-3.1-pro-preview | Google | 5 896 | 🔺 +60 |
| 2 | gpt-5.6-luna | OpenAI | 4 463 | 🔺 +396 |
| 3 | DeepSeek V4 Flash 0731 | DeepSeek | 2 850 | 🔺 +2 200 |
| 4 | gpt-5.5 | OpenAI | 2 264 | 🔻 -37 |
| 5 | deepseek-v4-pro | DeepSeek | 1 982 | 🔺 +74 |
| 6 | gpt-5.6-terra | OpenAI | 1 971 | 🔺 +259 |
| 7 | claude-sonnet-4-6 | Anthropic | 1 721 | 🔺 +18 |
| 8 | claude-opus-4-7 | Anthropic | 1 705 | 🔺 +353 |
| 9 | claude-opus-5 | Anthropic | 1 441 | 🔺 +154 |
| 10 | gpt-5.6-sol | OpenAI | 1 079 | 🔺 +23 |
| 11 | claude-sonnet-5 | Anthropic | 947 | 🔺 +51 |
| 12 | gemini-3-flash-preview | Google | 884 | 0 |
| 13 | claude-opus-4-8 | Anthropic | 881 | 🔺 +35 |
| 14 | gemini-3.6-flash | Google | 844 | 🔺 +125 |
| 15 | gpt-5.4-mini | OpenAI | 773 | 🔺 +26 |
| 16 | gpt-5-nano | OpenAI | 683 | 0 |
| 17 | gemini-3.1-flash-lite | Google | 659 | 🔺 +28 |
| 18 | gpt-5.4 | OpenAI | 580 | 🔻 -4 |
| 19 | gpt-5-mini | OpenAI | 565 | 🔻 -42 |
| 20 | kimi-k3 | Moonshot | 331 | 🔻 -18 |
| 21 | GLM-5.2 | Zhipu | 315 | 🔺 +2 |
| 22 | deepseek-v4-flash | DeepSeek | 311 | 🔻 -4 |
| 23 | Qwen 3.7 Flash | Alibaba | 217 | 🔺 +212 |
| 24 | text-embedding-3-small | OpenAI | 188 | 🔺 +1 |
| 25 | Aion 3.0 | Aion Labs | 140 | 0 |
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

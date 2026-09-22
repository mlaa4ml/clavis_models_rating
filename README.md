# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-22 (UTC) · моделей в рейтинге: 125_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gpt-5.6-luna@CodexPro | OpenAI | 15 881 | 🔺 +1 167 |
| 2 | Hy3 | Tencent | 12 061 | 0 |
| 3 | gpt-4.1-mini | OpenAI | 10 124 | 🔺 +349 |
| 4 | gemini-3.1-flash-lite-r | Google | 8 267 | 0 |
| 5 | gemini-3.1-pro-preview | Google | 6 642 | 🔻 -79 |
| 6 | gpt-5.6-terra@azureopenai | OpenAI | 5 989 | 🔻 -15 |
| 7 | gemini-3.8-flash@gemini | Google | 4 454 | 🔺 +65 |
| 8 | gpt-5.6-sol@Azure | OpenAI | 3 573 | 🔻 -52 |
| 9 | text-embedding-3-small@Azure | OpenAI | 2 483 | 🔻 -427 |
| 10 | gemini-3.7-flash@gemini | Google | 2 422 | 🔻 -258 |
| 11 | gpt-5.5@CodexPro | OpenAI | 1 887 | 🔺 +31 |
| 12 | glm-5.3-flash@Temp | Zhipu | 1 727 | 🔺 +418 |
| 13 | gpt-6-astra@codex | OpenAI | 1 656 | 🔺 +4 |
| 14 | claude-opus-5 | Anthropic | 1 541 | 🔻 -61 |
| 15 | claude-sonnet-5@Kiro | Anthropic | 931 | 🔺 +1 |
| 16 | gpt-4o-mini | OpenAI | 755 | 🔻 -8 |
| 17 | Claude Opus 4.8 | Anthropic | 729 | 🔺 +1 |
| 18 | glm-5.3@Temp | Zhipu | 578 | 🔺 +244 |
| 19 | gemini-3.6-flash@geminipro | Google | 569 | 🔻 -7 |
| 20 | gpt-5-mini | OpenAI | 504 | 🔺 +55 |
| 21 | claude-sonnet-4-6@Kiro | Anthropic | 480 | 🔻 -3 |
| 22 | deepseek-v4-pro@Deepseek | DeepSeek | 479 | 🔺 +34 |
| 23 | gpt-5.4-mini@Azure | OpenAI | 331 | 🔻 -3 |
| 24 | [free]kimi-k3@request | Moonshot | 286 | 🔺 +1 |
| 25 | gpt-4o | OpenAI | 261 | 🔻 -1 |
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

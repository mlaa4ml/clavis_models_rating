# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-23 (UTC) · моделей в рейтинге: 128_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gpt-5.6-luna@CodexPro | OpenAI | 16 055 | 🔺 +174 |
| 2 | Hy3 | Tencent | 12 061 | 0 |
| 3 | gpt-4.1-mini | OpenAI | 10 484 | 🔺 +360 |
| 4 | gemini-3.1-flash-lite-r | Google | 8 267 | 0 |
| 5 | gemini-3.1-pro-preview | Google | 6 642 | 0 |
| 6 | gpt-5.6-terra@azureopenai | OpenAI | 5 787 | 🔻 -202 |
| 7 | gemini-3.8-flash@gemini | Google | 4 523 | 🔺 +69 |
| 8 | gpt-5.6-sol@Azure | OpenAI | 3 430 | 🔻 -143 |
| 9 | gemini-3.7-flash@gemini | Google | 2 421 | 🔻 -1 |
| 10 | text-embedding-3-small@Azure | OpenAI | 2 315 | 🔻 -168 |
| 11 | gpt-5.5@CodexPro | OpenAI | 1 905 | 🔺 +18 |
| 12 | glm-5.3-flash@Temp | Zhipu | 1 764 | 🔺 +37 |
| 13 | gpt-6-astra@codex | OpenAI | 1 657 | 🔺 +1 |
| 14 | claude-opus-5@ClaudeLite | Anthropic | 1 609 | 🔺 +68 |
| 15 | Claude Opus 4.8 | Anthropic | 1 088 | 🔺 +359 |
| 16 | claude-sonnet-5 | Anthropic | 929 | 🔻 -2 |
| 17 | gpt-4o-mini | OpenAI | 754 | 🔻 -1 |
| 18 | glm-5.3@Temp | Zhipu | 654 | 🔺 +76 |
| 19 | gpt-5-mini | OpenAI | 621 | 🔺 +117 |
| 20 | gemini-3.6-flash@geminipro | Google | 541 | 🔻 -28 |
| 21 | [req]deepseek-v4-pro | DeepSeek | 479 | 0 |
| 22 | [req]claude-sonnet-4-6 | Anthropic | 477 | 🔻 -3 |
| 23 | gpt-5.4-mini@Azure | OpenAI | 331 | 0 |
| 24 | [free]kimi-k3@request | Moonshot | 298 | 🔺 +12 |
| 25 | gpt-4o | OpenAI | 261 | 0 |
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

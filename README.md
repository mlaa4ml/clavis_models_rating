# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-10 (UTC) · моделей в рейтинге: 185_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gpt-5.6-luna@Azure | OpenAI | 11 665 | 🔺 +156 |
| 2 | gemini-3.1-flash-lite@GeminiVertex | Google | 7 756 | 🔺 +172 |
| 3 | DeepSeek V4 Flash 0731 | DeepSeek | 6 798 | 🔺 +6 754 |
| 4 | gpt-5.6-terra | OpenAI | 4 955 | 🔻 -473 |
| 5 | gpt-4.1-mini | OpenAI | 4 864 | 🔺 +12 |
| 6 | Hy3 | Tencent | 3 794 | 🔺 +127 |
| 7 | Qwen3.7 Flash | Alibaba | 3 701 | — |
| 8 | gemini-3.1-pro-preview@GeminiVertex | Google | 3 313 | 🔺 +5 |
| 9 | [free]gpt-5.6-sol@request | OpenAI | 2 627 | 🔺 +62 |
| 10 | text-embedding-3-small | OpenAI | 2 576 | 🔺 +11 |
| 11 | [free]claude-opus-5@request | Anthropic | 1 386 | 🔺 +198 |
| 12 | claude-opus-4-7-r | Anthropic | 1 125 | 🔻 -64 |
| 13 | glm-5.3-flash@Temp | Zhipu | 1 111 | 🔻 -133 |
| 14 | [req]glm-5.3 | Zhipu | 897 | 🔻 -149 |
| 15 | [req]glm-5.1 | Zhipu | 806 | 🔺 +3 |
| 16 | [free]gemini-3.7-flash@request | Google | 797 | 🔻 -196 |
| 17 | gpt-4o-mini | OpenAI | 746 | 0 |
| 18 | claude-sonnet-5@ClaudeMix | Anthropic | 548 | 🔻 -400 |
| 19 | [req]gemini-3.6-flash | Google | 514 | 🔺 +45 |
| 20 | [req]deepseek-v4-flash | DeepSeek | 431 | 🔺 +297 |
| 21 | gpt-6-astra@codex | OpenAI | 421 | 🔺 +72 |
| 22 | gemini-3.8-flash@GeminiVertex | Google | 343 | 🔺 +19 |
| 23 | claude-sonnet-4-6@claudecode | Anthropic | 326 | 🔺 +68 |
| 24 | DeepSeek V4 Pro | DeepSeek | 277 | 🔻 -29 |
| 25 | claude-opus-4-8@claudecodecheap | Anthropic | 266 | 🔺 +31 |
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

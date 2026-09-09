# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-09 (UTC) · моделей в рейтинге: 138_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | GPT 5.6 Luna | OpenAI | 11 509 | 🔺 +614 |
| 2 | gemini-3.1-flash-lite@geminipro | Google | 7 584 | 🔺 +71 |
| 3 | gpt-5.6-terra | OpenAI | 5 428 | 🔺 +482 |
| 4 | gpt-4.1-mini | OpenAI | 4 852 | 🔺 +8 |
| 5 | Hy3 | Tencent | 3 667 | 🔺 +81 |
| 6 | Gemini 3.1 Pro Preview | Google | 3 308 | 🔺 +55 |
| 7 | [free]gpt-5.6-sol@request | OpenAI | 2 565 | 🔻 -195 |
| 8 | text-embedding-3-small | OpenAI | 2 565 | 🔺 +26 |
| 9 | glm-5.3-flash@Temp | Zhipu | 1 244 | 🔺 +115 |
| 10 | claude-opus-4-7@ClaudeMix | Anthropic | 1 189 | 🔻 -10 |
| 11 | [free]claude-opus-5@request | Anthropic | 1 188 | 🔺 +244 |
| 12 | [req]glm-5.3 | Zhipu | 1 046 | 0 |
| 13 | [free]gemini-3.7-flash@request | Google | 993 | 🔺 +171 |
| 14 | claude-sonnet-5@ClaudeMix | Anthropic | 948 | 🔺 +9 |
| 15 | GLM 5.1 | Zhipu | 803 | 🔺 +166 |
| 16 | gpt-4o-mini | OpenAI | 746 | 0 |
| 17 | Gemini 3.1 Flash Lite Preview | Google | 495 | 0 |
| 18 | [req]gemini-3.6-flash | Google | 469 | 0 |
| 19 | [free]deepseek-v4-pro-0813@request | DeepSeek | 459 | 🔺 +18 |
| 20 | gpt-6-astra@codex | OpenAI | 349 | 🔺 +302 |
| 21 | gpt-5.5@CodexPro | OpenAI | 340 | 🔺 +9 |
| 22 | gemini-3.8-flash@geminipro | Google | 324 | 🔺 +13 |
| 23 | deepseek-v4-pro@Deepseek | DeepSeek | 306 | 🔺 +134 |
| 24 | claude-sonnet-4-6@claudecode | Anthropic | 258 | 🔺 +6 |
| 25 | grok-4.5@GrokBuild | xAI | 249 | 🔺 +92 |
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

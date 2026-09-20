# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-20 (UTC) · моделей в рейтинге: 133_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gpt-5.6-luna@CodexPro | OpenAI | 15 601 | 🔺 +190 |
| 2 | Hy3 | Tencent | 12 061 | 🔻 -3 |
| 3 | gpt-4.1-mini | OpenAI | 9 395 | 🔺 +359 |
| 4 | gemini-3.1-flash-lite-r | Google | 8 032 | 🔺 +85 |
| 5 | gemini-3.1-pro-preview@request | Google | 6 721 | 🔺 +127 |
| 6 | gpt-5.6-terra@azureopenai | OpenAI | 6 231 | 🔻 -123 |
| 7 | gemini-3.8-flash@gemini | Google | 4 008 | 🔺 +481 |
| 8 | [free]gpt-5.6-sol@request | OpenAI | 3 669 | 🔻 -252 |
| 9 | [free]GLM-5.3-flash@request | Zhipu | 3 286 | 🔺 +1 982 |
| 10 | text-embedding-3-small@Azure | OpenAI | 2 978 | 🔻 -31 |
| 11 | gpt-5.5@CodexPro | OpenAI | 1 920 | 🔺 +24 |
| 12 | gpt-6-astra@codex | OpenAI | 1 650 | 🔺 +24 |
| 13 | claude-opus-5 | Anthropic | 1 607 | 🔻 -85 |
| 14 | [free]gemini-3.7-flash@request | Google | 1 364 | 🔺 +10 |
| 15 | glm-5.3-flash@Temp | Zhipu | 1 308 | 🔺 +28 |
| 16 | [free]GLM-5.3@request | Zhipu | 1 053 | 🔺 +70 |
| 17 | claude-sonnet-5 | Anthropic | 927 | 🔻 -7 |
| 18 | gpt-4o-mini | OpenAI | 762 | 🔺 +16 |
| 19 | [free]deepseek-v4-pro-0813@request | DeepSeek | 747 | 🔺 +68 |
| 20 | claude-opus-4-8@request | Anthropic | 718 | 0 |
| 21 | gemini-3.6-flash@geminipro | Google | 601 | 🔺 +42 |
| 22 | [req]claude-sonnet-4-6 | Anthropic | 488 | 🔻 -17 |
| 23 | gpt-5-mini | OpenAI | 449 | 🔺 +1 |
| 24 | [req]deepseek-v4-pro | DeepSeek | 427 | 0 |
| 25 | gpt-5.4-mini@Azure | OpenAI | 354 | 🔺 +196 |
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

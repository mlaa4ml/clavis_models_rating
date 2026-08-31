# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-31 (UTC) · моделей в рейтинге: 132_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | [free]claude-opus-5@request | Anthropic | 60 251 | 🔺 +23 491 |
| 2 | GPT 5.6 Luna | OpenAI | 6 759 | 🔺 +1 497 |
| 3 | gemini-3.1-flash-lite@geminipro | Google | 6 142 | 🔺 +957 |
| 4 | gpt-4.1-mini | OpenAI | 3 771 | 🔺 +3 756 |
| 5 | gpt-5.6-terra@CodexPro | OpenAI | 2 503 | 🔺 +197 |
| 6 | Gemini 3.1 Pro Preview | Google | 2 441 | 🔺 +153 |
| 7 | gpt-5.6-sol@Azure | OpenAI | 1 951 | 🔺 +62 |
| 8 | claude-opus-4-7@ClaudeLite | Anthropic | 1 193 | 🔻 -231 |
| 9 | Hy3 | Tencent | 1 018 | 🔺 +324 |
| 10 | gemini-3-flash-preview | Google | 880 | 🔻 -6 |
| 11 | text-embedding-3-small@Azure | OpenAI | 759 | 🔺 +4 |
| 12 | gpt-4o-mini | OpenAI | 732 | 🔺 +6 |
| 13 | [req]glm-5.1 | Zhipu | 588 | 🔺 +212 |
| 14 | [req]gemini-3.7-flash@request | Google | 569 | 🔺 +9 |
| 15 | gemini-3.6-flash@geminipro | Google | 499 | 🔺 +8 |
| 16 | Gemini 3.1 Flash Lite Preview | Google | 491 | 🔺 +488 |
| 17 | claude-sonnet-5-r | Anthropic | 412 | 🔺 +165 |
| 18 | gpt-5.4-mini@CodexPro | OpenAI | 347 | 🔺 +1 |
| 19 | gpt-5.5@CodexPro | OpenAI | 259 | 🔺 +28 |
| 20 | [free]deepseek-v4-pro-0813@request | DeepSeek | 227 | 🔺 +224 |
| 21 | GLM 5.3 | Zhipu | 223 | 0 |
| 22 | DeepSeek V4 Flash | DeepSeek | 218 | 🔺 +17 |
| 23 | gpt-4o | OpenAI | 188 | 0 |
| 24 | claude-opus-4-8@ClaudeLite | Anthropic | 156 | 🔺 +25 |
| 25 | DeepSeek V4 Pro | DeepSeek | 105 | 🔺 +7 |
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

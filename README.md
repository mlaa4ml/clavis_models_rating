# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-02 (UTC) · моделей в рейтинге: 138_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | [free]claude-opus-5@request | Anthropic | 108 704 | 🔺 +25 213 |
| 2 | GPT 5.6 Luna | OpenAI | 8 060 | 🔺 +703 |
| 3 | gemini-3.1-flash-lite@geminipro | Google | 7 321 | 🔺 +356 |
| 4 | gpt-4.1-mini | OpenAI | 3 787 | 🔺 +10 |
| 5 | gpt-5.6-terra@CodexPro | OpenAI | 2 615 | 🔺 +6 |
| 6 | [req]gemini-3.1-pro-preview | Google | 2 546 | 🔺 +24 |
| 7 | gpt-5.6-sol@Azure | OpenAI | 1 994 | 🔺 +19 |
| 8 | Hy3 | Tencent | 1 854 | 🔺 +701 |
| 9 | Claude Opus 4.7 | Anthropic | 1 188 | 🔻 -3 |
| 10 | text-embedding-3-small@Azure | OpenAI | 832 | 🔺 +15 |
| 11 | gpt-4o-mini@Azure | OpenAI | 732 | 0 |
| 12 | gemini-3.7-flash-r | Google | 642 | 🔺 +27 |
| 13 | [req]glm-5.1 | Zhipu | 588 | 0 |
| 14 | claude-sonnet-5-r | Anthropic | 543 | 🔺 +41 |
| 15 | Gemini 3.1 Flash Lite Preview | Google | 491 | 0 |
| 16 | gemini-3.6-flash-r | Google | 488 | 🔻 -2 |
| 17 | GLM 5.3 | Zhipu | 478 | 🔺 +93 |
| 18 | [free]deepseek-v4-pro-0813@request | DeepSeek | 373 | 🔺 +70 |
| 19 | gemini-3-flash-preview-r | Google | 347 | 🔻 -539 |
| 20 | gpt-5.4-mini@Azure | OpenAI | 347 | 0 |
| 21 | gpt-5.5@CodexPro | OpenAI | 329 | 🔺 +24 |
| 22 | claude-opus-4-8@ClaudeLite | Anthropic | 253 | 🔺 +70 |
| 23 | deepseek-v4-flash@Deepseek | DeepSeek | 230 | 🔻 -1 |
| 24 | gpt-4o | OpenAI | 209 | 0 |
| 25 | grok-4.5@GrokBuild | xAI | 117 | 🔺 +80 |
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

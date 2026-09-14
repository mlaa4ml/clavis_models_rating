# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-14 (UTC) · моделей в рейтинге: 129_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gpt-5.6-luna@Azure | OpenAI | 13 131 | 🔺 +391 |
| 2 | gemini-3.1-flash-lite | Google | 7 920 | 0 |
| 3 | gpt-4.1-mini | OpenAI | 7 480 | 🔺 +377 |
| 4 | gemini-3.1-pro-preview | Google | 6 086 | 🔺 +561 |
| 5 | gpt-5.6-terra | OpenAI | 5 987 | 🔺 +88 |
| 6 | Hy3 | Tencent | 4 018 | 🔺 +5 |
| 7 | [free]gpt-5.6-sol@request | OpenAI | 3 243 | 🔺 +176 |
| 8 | text-embedding-3-small | OpenAI | 2 707 | 🔺 +115 |
| 9 | gemini-3.8-flash@GeminiVertex | Google | 2 683 | 🔺 +1 769 |
| 10 | gpt-6-astra@codex | OpenAI | 1 568 | 🔺 +38 |
| 11 | [free]claude-opus-5@request | Anthropic | 1 409 | 🔺 +12 |
| 12 | glm-5.3-flash@Temp | Zhipu | 1 162 | 🔺 +4 |
| 13 | claude-opus-4-7@ClaudeMax | Anthropic | 995 | 🔻 -36 |
| 14 | glm-5.3@Temp | Zhipu | 991 | 0 |
| 15 | [free]gemini-3.7-flash@request | Google | 932 | 🔺 +1 |
| 16 | [free]GLM-5.3-flash@request | Zhipu | 912 | 🔺 +305 |
| 17 | [req]glm-5.1 | Zhipu | 806 | 0 |
| 18 | claude-sonnet-5@claudecodecheap | Anthropic | 757 | 🔺 +2 |
| 19 | gpt-4o-mini | OpenAI | 746 | 0 |
| 20 | [free]GLM-5.3@request | Zhipu | 560 | 🔺 +103 |
| 21 | gpt-5.5@CodexPro | OpenAI | 543 | 🔺 +10 |
| 22 | claude-opus-4-8@ClaudeLite | Anthropic | 519 | 🔺 +33 |
| 23 | [req]gemini-3.6-flash | Google | 517 | 0 |
| 24 | deepseek-v4-pro@Deepseek | DeepSeek | 410 | 0 |
| 25 | claude-sonnet-4-6@claudecode | Anthropic | 371 | 🔺 +31 |
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

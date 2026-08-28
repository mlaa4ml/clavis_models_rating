# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-28 (UTC) · моделей в рейтинге: 123_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | Claude Opus 5 | Anthropic | 9 027 | 🔺 +4 499 |
| 2 | gpt-5.6-luna@Azure | OpenAI | 4 679 | 🔺 +1 997 |
| 3 | gemini-3.1-pro-preview@gemini | Google | 2 226 | 🔺 +150 |
| 4 | gpt-5.6-terra@CodexPro | OpenAI | 1 986 | 🔺 +225 |
| 5 | gpt-5.6-sol@Azure | OpenAI | 1 698 | 🔺 +82 |
| 6 | claude-opus-4-7@ClaudeMax | Anthropic | 1 383 | 🔻 -60 |
| 7 | gemini-3-flash-preview@geminipro | Google | 882 | 🔺 +3 |
| 8 | text-embedding-3-small@Azure | OpenAI | 744 | 🔺 +10 |
| 9 | [req]gemini-3.7-flash@request | Google | 547 | 🔺 +25 |
| 10 | Hy3 | Tencent | 392 | 🔺 +341 |
| 11 | gpt-4o-mini | OpenAI | 377 | 🔺 +354 |
| 12 | gpt-5.4-mini@Azure | OpenAI | 346 | 🔺 +34 |
| 13 | gemini-3.6-flash@geminipro | Google | 200 | 🔺 +5 |
| 14 | gpt-5.5@CodexPro | OpenAI | 191 | 🔺 +5 |
| 15 | DeepSeek V4 Flash | DeepSeek | 175 | 🔺 +169 |
| 16 | Claude Opus 4.8 | Anthropic | 116 | 🔺 +13 |
| 17 | glm-5.3@Temp | Zhipu | 111 | 🔺 +94 |
| 18 | gemini-3.1-flash-lite@geminipro | Google | 111 | 🔺 +99 |
| 19 | claude-sonnet-4-6@claudecodecheap | Anthropic | 110 | 🔻 -23 |
| 20 | gemini-2.5-flash@gemini | Google | 99 | 🔺 +2 |
| 21 | gpt-5.4@azureopenai | OpenAI | 88 | 🔺 +8 |
| 22 | claude-sonnet-5 | Anthropic | 63 | 🔺 +1 |
| 23 | gemini-2.5-pro | Google | 57 | 🔺 +8 |
| 24 | claude-fable-5@claudecode | Anthropic | 46 | 🔺 +33 |
| 25 | gpt-5-mini@Azure | OpenAI | 40 | 🔺 +3 |
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

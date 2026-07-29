# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
(суммарное число запросов за последние 30 дней, по данным `total_requests`
из `https://api.clavis.to/catalog/model/{id}`) и раз в день обновляет
таблицу ниже через GitHub Actions.

Полная история по дням — в [`data/history.csv`](data/history.csv).
Снапшоты за каждый день — в [`data/snapshots/`](data/snapshots/).

## Текущий рейтинг

<!-- RATING_TABLE_START -->
_Обновлено: 2026-07-29 (UTC) · моделей в рейтинге: 129_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gpt-5.6-sol | OpenAI | 4 252 | 🔺 +33 |
| 2 | gemini-3.1-pro-preview | Google | 3 363 | 🔺 +238 |
| 3 | gpt-5.5 | OpenAI | 1 949 | 🔻 -119 |
| 4 | claude-opus-4-8 | Anthropic | 1 592 | 🔻 -79 |
| 5 | deepseek-v4-pro | DeepSeek | 1 579 | 🔺 +123 |
| 6 | gpt-5.6-luna | OpenAI | 1 566 | 🔺 +522 |
| 7 | deepseek-v4-flash | DeepSeek | 1 476 | 🔺 +12 |
| 8 | gpt-5-mini | OpenAI | 1 178 | 🔺 +48 |
| 9 | gpt-5.4-mini | OpenAI | 1 163 | 🔺 +3 |
| 10 | gpt-5.4 | OpenAI | 961 | 🔺 +11 |
| 11 | gemini-3.1-flash-lite | Google | 763 | 🔺 +122 |
| 12 | gemini-3-flash-preview | Google | 754 | 0 |
| 13 | claude-opus-4-7 | Anthropic | 698 | 🔺 +13 |
| 14 | gpt-5-nano | OpenAI | 673 | 🔺 +407 |
| 15 | gemini-3.5-flash | Google | 579 | 0 |
| 16 | claude-opus-5 | Anthropic | 574 | 🔺 +127 |
| 17 | claude-sonnet-4-6 | Anthropic | 371 | 🔻 -338 |
| 18 | claude-fable-5 | Anthropic | 294 | 🔻 -27 |
| 19 | gemini-2.5-pro | Google | 282 | 0 |
| 20 | gpt-4o-mini | OpenAI | 267 | 0 |
| 21 | claude-sonnet-5 | Anthropic | 225 | 0 |
| 22 | text-embedding-3-small | OpenAI | 203 | 0 |
| 23 | Aion 3.0 | Aion Labs | 161 | 0 |
| 24 | gpt-5.6-terra | OpenAI | 152 | 0 |
| 25 | gemini-embedding-001 | Google | 116 | 🔺 +10 |
<!-- RATING_TABLE_END -->

## Как это работает

1. `.github/workflows/daily-rating.yml` запускается каждый день по расписанию
   (см. cron в файле) и может быть запущен вручную через вкладку **Actions**.
2. `scripts/collect.py` тянет список моделей и статистику запросов из
   публичного API Clavis.to, сохраняет:
   - `data/snapshots/YYYY-MM-DD.csv` — срез за конкретный день;
   - `data/snapshots/errors_YYYY-MM-DD.csv` — модели, по которым не удалось
     получить данные;
   - `data/history.csv` — накопительная история (одна строка на модель на
     день), не перезаписывается, а дополняется.
3. `scripts/update_readme.py` читает `data/history.csv`, строит таблицу
   топ-25 моделей с дельтой к предыдущему дню и вставляет её в этот README
   между маркерами `RATING_TABLE_START` / `RATING_TABLE_END`.
4. Workflow коммитит и пушит изменения (`data/*` и `README.md`) обратно в
   репозиторий от имени `github-actions[bot]`.

## Локальный запуск

```bash
pip install -r requirements.txt
python scripts/collect.py
python scripts/update_readme.py
```

## Настройка расписания

По умолчанию — раз в день в 06:00 UTC. Поменять можно в
`.github/workflows/daily-rating.yml`, поле `cron`. Формат стандартный —
5 полей (минута, час, день месяца, месяц, день недели), время всегда в UTC.

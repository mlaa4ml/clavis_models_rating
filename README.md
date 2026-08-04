# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
(суммарное число запросов за последние 30 дней, по данным `total_requests`
из `https://api.clavis.to/catalog/model/{id}`) и раз в день обновляет
таблицу ниже через GitHub Actions.

Полная история по дням — в [`data/history.csv`](data/history.csv).
Снапшоты за каждый день — в [`data/snapshots/`](data/snapshots/).

## Текущий рейтинг

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-04 (UTC) · моделей в рейтинге: 132_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gemini-3.1-pro-preview | Google | 4 539 | 🔻 -9 |
| 2 | gpt-5.6-sol | OpenAI | 4 392 | 0 |
| 3 | deepseek-v4-pro | DeepSeek | 2 149 | 🔺 +15 |
| 4 | gpt-5.6-luna | OpenAI | 2 104 | 🔺 +42 |
| 5 | claude-sonnet-4-6 | Anthropic | 1 688 | 0 |
| 6 | deepseek-v4-flash | DeepSeek | 1 504 | 🔺 +16 |
| 7 | gemini-3-flash-preview | Google | 1 500 | 🔺 +132 |
| 8 | gpt-5.5 | OpenAI | 1 181 | 🔻 -49 |
| 9 | claude-opus-4-8 | Anthropic | 1 141 | 🔻 -174 |
| 10 | claude-opus-4-7 | Anthropic | 987 | 0 |
| 11 | gpt-5-mini | OpenAI | 974 | 🔻 -37 |
| 12 | gpt-5.4-mini | OpenAI | 959 | 🔻 -37 |
| 13 | gemini-3.1-flash-lite | Google | 752 | 0 |
| 14 | claude-opus-5 | Anthropic | 736 | 0 |
| 15 | gpt-5-nano | OpenAI | 679 | 0 |
| 16 | gemini-3.6-flash | Google | 609 | 0 |
| 17 | gpt-5.4 | OpenAI | 526 | 🔻 -41 |
| 18 | claude-sonnet-5 | Anthropic | 509 | 🔺 +42 |
| 19 | gpt-5.6-terra | OpenAI | 359 | 🔺 +187 |
| 20 | gemini-3.5-flash | Google | 296 | 🔻 -1 |
| 21 | gemini-2.5-pro | Google | 239 | 0 |
| 22 | text-embedding-3-small | OpenAI | 203 | 0 |
| 23 | claude-fable-5 | Anthropic | 178 | 🔻 -32 |
| 24 | Aion 3.0 | Aion Labs | 167 | 0 |
| 25 | gemini-embedding-001 | Google | 113 | 🔻 -3 |
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

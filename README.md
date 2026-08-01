# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
(суммарное число запросов за последние 30 дней, по данным `total_requests`
из `https://api.clavis.to/catalog/model/{id}`) и раз в день обновляет
таблицу ниже через GitHub Actions.

Полная история по дням — в [`data/history.csv`](data/history.csv).
Снапшоты за каждый день — в [`data/snapshots/`](data/snapshots/).

## Текущий рейтинг

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-01 (UTC) · моделей в рейтинге: 129_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gpt-5.6-sol | OpenAI | 4 350 | 🔺 +43 |
| 2 | gemini-3.1-pro-preview | Google | 3 975 | 🔺 +182 |
| 3 | deepseek-v4-pro | DeepSeek | 2 129 | 🔺 +3 |
| 4 | gpt-5.6-luna | OpenAI | 1 830 | 🔺 +71 |
| 5 | deepseek-v4-flash | DeepSeek | 1 478 | 0 |
| 6 | gpt-5.5 | OpenAI | 1 455 | 🔻 -204 |
| 7 | claude-opus-4-8 | Anthropic | 1 340 | 🔻 -97 |
| 8 | gpt-5-mini | OpenAI | 1 200 | 🔻 -53 |
| 9 | gpt-5.4-mini | OpenAI | 1 152 | 🔻 -13 |
| 10 | claude-opus-4-7 | Anthropic | 978 | 🔺 +235 |
| 11 | gemini-3.1-flash-lite | Google | 752 | 🔻 -15 |
| 12 | gemini-3-flash-preview | Google | 725 | 🔺 +6 |
| 13 | gpt-5-nano | OpenAI | 673 | 0 |
| 14 | claude-opus-5 | Anthropic | 661 | 🔺 +1 |
| 15 | gpt-5.4 | OpenAI | 608 | 🔻 -154 |
| 16 | gemini-3.6-flash | Google | 492 | 🔺 +383 |
| 17 | gemini-3.5-flash | Google | 384 | 🔻 -77 |
| 18 | claude-fable-5 | Anthropic | 332 | 🔺 +26 |
| 19 | gemini-2.5-pro | Google | 265 | 🔻 -17 |
| 20 | claude-sonnet-5 | Anthropic | 229 | 0 |
| 21 | text-embedding-3-small | OpenAI | 203 | 0 |
| 22 | gpt-5.6-terra | OpenAI | 172 | 🔺 +1 |
| 23 | Aion 3.0 | Aion Labs | 165 | 0 |
| 24 | claude-sonnet-4-6 | Anthropic | 137 | 🔻 -33 |
| 25 | gemini-embedding-001 | Google | 114 | 0 |
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

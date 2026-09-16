# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-16 (UTC) · моделей в рейтинге: 128_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | gpt-5.6-luna@azureopenai | OpenAI | 13 689 | 🔺 +331 |
| 2 | gpt-4.1-mini | OpenAI | 7 928 | 🔺 +418 |
| 3 | gemini-3.1-flash-lite@geminipro | Google | 7 926 | 0 |
| 4 | gemini-3.1-pro-preview@GeminiVertex | Google | 6 294 | 🔺 +82 |
| 5 | gpt-5.6-terra@azureopenai | OpenAI | 6 161 | 🔺 +39 |
| 6 | Hy3 | Tencent | 4 230 | 🔺 +56 |
| 7 | [free]gpt-5.6-sol@request | OpenAI | 3 484 | 🔺 +62 |
| 8 | gemini-3.8-flash@gemini | Google | 3 334 | 🔺 +536 |
| 9 | claude-opus-5@claudecode | Anthropic | 1 774 | 🔺 +360 |
| 10 | gpt-6-astra@azureopenai | OpenAI | 1 599 | 🔺 +15 |
| 11 | [free]gemini-3.7-flash@request | Google | 1 159 | 🔺 +229 |
| 12 | [free]GLM-5.3-flash@request | Zhipu | 1 035 | 🔺 +22 |
| 13 | claude-sonnet-5-r | Anthropic | 932 | 🔺 +179 |
| 14 | glm-5.3-flash@Temp | Zhipu | 903 | 🔻 -274 |
| 15 | gpt-4o-mini | OpenAI | 746 | 0 |
| 16 | claude-opus-4-8@ClaudeLite | Anthropic | 714 | 🔺 +178 |
| 17 | gpt-5.5@CodexPro | OpenAI | 641 | 🔺 +80 |
| 18 | [free]GLM-5.3@request | Zhipu | 628 | 🔺 +51 |
| 19 | gemini-3.6-flash@geminipro | Google | 510 | 🔻 -2 |
| 20 | claude-sonnet-4-6@claudecode | Anthropic | 496 | 🔺 +158 |
| 21 | deepseek-v4-pro | DeepSeek | 419 | 🔺 +9 |
| 22 | [free]deepseek-v4-pro-0813@request | DeepSeek | 326 | 🔺 +4 |
| 23 | claude-opus-4-7@ClaudeMax | Anthropic | 271 | 🔻 -194 |
| 24 | [free]kimi-k3@request | Moonshot | 259 | 🔺 +2 |
| 25 | gpt-4o | OpenAI | 257 | 0 |
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

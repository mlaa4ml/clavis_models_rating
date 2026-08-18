# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-08-18 (UTC) · моделей в рейтинге: 326_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | DeepSeek V4 Flash 0731 | DeepSeek | 4 713 | 🔺 +1 863 |
| 2 | Gemini 3.1 Pro Preview | Google | 849 | 🔻 -5 047 |
| 3 | Claude Sonnet 5 | Anthropic | 239 | 🔻 -708 |
| 4 | GPT-5.4 | OpenAI | 222 | 🔻 -358 |
| 5 | Qwen3.7 Flash | Alibaba | 217 | 0 |
| 6 | DeepSeek V4 Flash 0731 | DeepSeek | 155 | 🔻 -156 |
| 7 | Aion-3.0 | Aion Labs | 140 | 0 |
| 8 | Claude Sonnet 4.6 | Anthropic | 125 | 🔺 +125 |
| 9 | Hy3 | Tencent | 48 | 0 |
| 10 | GLM 5.2 | Zhipu | 45 | 🔻 -270 |
| 11 | Aion-2.0 | Aion Labs | 37 | 🔺 +15 |
| 12 | Qwen3.8 Max | Alibaba | 35 | 0 |
| 13 | Gemini 3.7 Flash | Google | 34 | 🔺 +27 |
| 14 | Qwen3 Coder Plus | Alibaba | 34 | 0 |
| 15 | Claude Haiku 4.5 | Anthropic | 20 | 🔺 +20 |
| 16 | Qwen3-VL Flash | Alibaba | 17 | 🔺 +17 |
| 17 | Kimi K3 | Moonshot | 14 | 🔻 -317 |
| 18 | Krea 2 Turbo | Other | 14 | 0 |
| 19 | Voice Clone | Other | 14 | 0 |
| 20 | GPT-5.6 Luna | OpenAI | 13 | 🔻 -4 450 |
| 21 | Claude Sonnet 4.5 | Anthropic | 12 | 🔺 +12 |
| 22 | DeepSeek V3.2 | DeepSeek | 12 | 0 |
| 23 | GPT-5.6 Sol | OpenAI | 12 | 🔻 -1 067 |
| 24 | Voice TTS | Other | 12 | 0 |
| 25 | DeepSeek V4 Pro 0813 | DeepSeek | 11 | 🔻 -1 971 |
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

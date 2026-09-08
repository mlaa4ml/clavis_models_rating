# Clavis.to — рейтинг моделей по числу запросов

Автоматически собирает статистику по всем моделям [Clavis.to](https://clavis.to/models)
и раз в день обновляет таблицы через GitHub Actions.

📊 **[Расширенные рейтинги → GitHub Pages](https://mlaa4ml.github.io/clavis_models_rating/)**
_(замени YOUR_USERNAME на свой GitHub login и включи Pages из ветки `main`, папки `docs/`)_

## Текущий рейтинг (по запросам за 30 дней)

<!-- RATING_TABLE_START -->
_Обновлено: 2026-09-08 (UTC) · моделей в рейтинге: 133_

| # | Модель | Провайдер | Запросов (30 дн.) | Δ к пред. дню |
|---|--------|-----------|-------------------:|--------------:|
| 1 | GPT 5.6 Luna | OpenAI | 10 895 | 🔺 +987 |
| 2 | gemini-3.1-flash-lite | Google | 7 513 | 🔺 +48 |
| 3 | GPT 5.6 Terra | OpenAI | 4 946 | 🔺 +966 |
| 4 | gpt-4.1-mini | OpenAI | 4 844 | 🔺 +40 |
| 5 | Hy3 | Tencent | 3 586 | 🔺 +77 |
| 6 | Gemini 3.1 Pro Preview | Google | 3 253 | 🔺 +115 |
| 7 | [free]gpt-5.6-sol@request | OpenAI | 2 760 | 🔺 +495 |
| 8 | text-embedding-3-small | OpenAI | 2 539 | 🔺 +67 |
| 9 | claude-opus-4-7@ClaudeMax | Anthropic | 1 199 | 🔺 +35 |
| 10 | glm-5.3-flash@Temp | Zhipu | 1 129 | 🔺 +154 |
| 11 | glm-5.3@Temp | Zhipu | 1 046 | 🔺 +166 |
| 12 | [free]claude-opus-5@request | Anthropic | 944 | 🔺 +96 |
| 13 | claude-sonnet-5-r | Anthropic | 939 | 🔺 +452 |
| 14 | [free]gemini-3.7-flash@request | Google | 822 | 🔺 +165 |
| 15 | gpt-4o-mini | OpenAI | 746 | 🔺 +4 |
| 16 | GLM 5.1 | Zhipu | 637 | 🔺 +30 |
| 17 | gemini-3.1-flash-lite-preview@geminipro | Google | 495 | 🔺 +415 |
| 18 | [req]gemini-3.6-flash | Google | 469 | 0 |
| 19 | [free]deepseek-v4-pro-0813@request | DeepSeek | 441 | 🔺 +391 |
| 20 | gpt-5.5@CodexPro | OpenAI | 331 | 🔺 +100 |
| 21 | gemini-3.8-flash@geminipro | Google | 311 | 🔺 +6 |
| 22 | claude-sonnet-4-6@claudecode | Anthropic | 252 | 🔺 +100 |
| 23 | [free]kimi-k3@request | Moonshot | 245 | 🔺 +10 |
| 24 | gpt-4o | OpenAI | 220 | 0 |
| 25 | claude-opus-4-8@claudecodecheap | Anthropic | 218 | 🔺 +40 |
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

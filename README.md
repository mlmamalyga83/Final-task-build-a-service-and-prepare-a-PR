# LLM Summarizer

Сервис для суммаризации текста с использованием LLM (OpenAI, Anthropic, YandexGPT и других совместимых API). Принимает текст через HTTP API, возвращает краткое содержание. Production-like подход: CI, конфигурация через переменные окружения, кеширование, обработка ошибок.

## Архитектура

```
main.py                 — точка входа (FastAPI + uvicorn)
api/routes.py           — HTTP-эндпоинт POST /process
services/summarizer.py  — бизнес-логика (пайплайн обработки)
services/cache.py       — кеш с TTL (dict-based)
llm/prompts.py          — шаблоны промптов
llm/client.py           — HTTP-клиент для вызова LLM
config/settings.py      — загрузка конфигурации из .env
```

## Установка и запуск

1. **Клонировать репозиторий и перейти в папку проекта**

2. **Создать виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Установить зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настроить переменные окружения:**
   ```bash
   cp .env.example .env
   ```
   Отредактировать `.env`, указать `LLM_API_KEY`.

5. **Запустить сервис:**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   или
   ```bash
   python main.py
   ```

## API

### `POST /process`

**Запрос:**
```json
{
  "text": "Ваш длинный текст для суммаризации..."
}
```

**Успешный ответ (200):**
```json
{
  "summary": "Краткое содержание текста...",
  "model": "gpt-3.5-turbo",
  "cached": false
}
```

**Ошибка валидации (422):**
```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": ["body", "text"],
      "msg": "String should have at least 1 character",
      "input": ""
    }
  ]
}
```

**Ошибка сервиса (503) — fallback:**
```json
{
  "summary": "⚠️ Сервис временно недоступен. Пожалуйста, попробуйте позже.",
  "model": "fallback",
  "cached": false
}
```

## Примеры запросов

```bash
# Успешный запрос
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Искусственный интеллект (ИИ) — это область компьютерных наук, занимающаяся созданием систем, способных выполнять задачи, требующие человеческого интеллекта. Такие системы могут обучаться на данных, распознавать образы, принимать решения и взаимодействовать с естественным языком."}'

# Ошибка валидации — пустой текст
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

## Переменные окружения

| Переменная | По умолчанию | Описание |
|---|---|---|
| `LLM_API_KEY` | — | Ключ API LLM-провайдера |
| `LLM_MODEL` | `gpt-3.5-turbo` | Модель для суммаризации |
| `LLM_BASE_URL` | `https://api.openai.com/v1` | Базовый URL API |
| `LLM_TIMEOUT` | `30` | Таймаут запроса (сек) |
| `LLM_MAX_TOKENS` | `500` | Максимум токенов в ответе |
| `LLM_TEMPERATURE` | `0.7` | Температура модели |
| `CACHE_TTL` | `3600` | Время жизни кеша (сек) |
| `LOG_LEVEL` | `INFO` | Уровень логирования |

## Тестирование

```bash
pytest -v
```

## Демонстрация работы

Скриншоты и примеры запросов для каждого сценария — в [TESTING.md](TESTING.md).

## CI

Настроен GitHub Actions (`.github/workflows/ci.yml`):
- линтинг (ruff)
- проверка загрузки конфигурации
- запуск тестов

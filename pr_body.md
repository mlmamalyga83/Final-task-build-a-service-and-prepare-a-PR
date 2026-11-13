## Цель изменений

Реализация итогового задания курса — end-to-end LLM-сервис для суммаризации текста с production-like подходом.

## Архитектура решения

Сервис имеет четырёхуровневую архитектуру:

1. **API-слой (api/routes.py)** — HTTP-эндпоинт POST /process на FastAPI, валидация через Pydantic
2. **Бизнес-логика (services/summarizer.py)** — пайплайн: валидация → проверка кеша → вызов LLM → пост-обработка → fallback
3. **LLM-модуль (llm/client.py, llm/prompts.py)** — формирование промпта, HTTP-вызов модели, обработка таймаутов и сетевых ошибок
4. **Конфигурация (config/settings.py)** — pydantic-settings, загрузка из .env, никакого хардкода

Дополнительно:
- Кеш с TTL (services/cache.py) на in-memory dict + SHA256-ключи
- Логирование ключевых этапов (INFO/ERROR/DEBUG)
- CI-пайплайн (GitHub Actions): ruff → проверка конфига → pytest

## Поток данных

```
Запрос → POST /process → валидация → кеш? (hit → ответ)
                                         miss → промпт → LLM API → пост-обработка → кеш → ответ
```

## Основные компоненты

- `main.py` — точка входа, lifespan, инициализация сервиса
- `api/routes.py` — POST /process, ProcessRequest/ProcessResponse схемы
- `services/summarizer.py` — Summarizer.process(), fallback, пост-обработка
- `services/cache.py` — TTLCache с dict + time.time()
- `llm/client.py` — call_llm() через httpx, LLMError
- `llm/prompts.py` — SYSTEM_PROMPT, build_prompt()
- `config/settings.py` — Settings с env_file
- `.github/workflows/ci.yml` — lint + test + config check

## Чек-лист самопроверки

- [x] Сервис запускается локально одной командой (`uvicorn main:app --reload`)
- [x] README содержит полную инструкцию по установке и запуску
- [x] Структура проекта логична: api/, services/, llm/, config/, tests/
- [x] Валидация входных данных (пустой текст, >10000 символов → 422)
- [x] Обработка сетевых ошибок и таймаутов при вызове LLM
- [x] Fallback-ответ при недоступности внешнего сервиса (503)
- [x] Корректные HTTP-статусы: 200, 422, 500
- [x] Логирование ключевых этапов с уровнями (INFO, ERROR, DEBUG)
- [x] Кеш для повторяющихся запросов с TTL
- [x] Логирование cache hit/miss
- [x] Настройки через переменные окружения (.env)
- [x] .env не в репозитории (в .gitignore)
- [x] .env.example с шаблоном переменных
- [x] API-ключи отсутствуют в коде
- [x] CI настроен (GitHub Actions): ruff → проверка конфига → pytest
- [x] CI проходит успешно (9 тестов)
- [x] Описание API в README с примерами запросов curl
- [x] Тесты: успешный сценарий, ошибка ввода, fallback, кеш
- [x] requirements.txt со всеми зависимостями
- [x] Pull Request с описанием архитектуры и чек-листом

# Тестирование и демонстрация работы сервиса

## 1. Успешный запрос

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Искусственный интеллект (ИИ) — это область компьютерных наук, занимающаяся созданием систем, способных выполнять задачи, требующие человеческого интеллекта. Такие системы могут обучаться на данных, распознавать образы, принимать решения и взаимодействовать с естественным языком."}'
```

**Ожидаемый ответ (200):**
```json
{
  "summary": "Краткое содержание текста от LLM...",
  "model": "gpt-3.5-turbo",
  "cached": false
}
```

**Скриншот:** `screenshots/1-success.png`

---

## 2. Ошибка валидации — пустой текст

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": ""}'
```

**Ожидаемый ответ (422):**
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

**Скриншот:** `screenshots/2-validation-error.png`

---

## 3. Fallback — недоступность LLM

Временно установите неверный API-ключ в `.env`:
```
LLM_API_KEY=invalid_key_123
```

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Какой-то текст для проверки fallback."}'
```

**Ожидаемый ответ (200, но с fallback):**
```json
{
  "summary": "⚠️ Сервис временно недоступен. Пожалуйста, попробуйте позже.",
  "model": "fallback",
  "cached": false
}
```

**Скриншот:** `screenshots/3-fallback.png`

---

## 4. Кеш — повторный запрос

Верните корректный ключ в `.env`, выполните два одинаковых запроса подряд:

```bash
# Первый запрос
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Повторяющийся текст для проверки кеша."}'

# Второй запрос (должен быть быстрее)
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{"text": "Повторяющийся текст для проверки кеша."}'
```

**Ожидаемый ответ на второй запрос:**
```json
{
  "summary": "...",
  "model": "gpt-3.5-turbo",
  "cached": true
}
```

В логах сервера: `Cache hit`, `Cache miss` при первом запросе.

**Скриншот:** `screenshots/4-cache.png`

---

## 5. CI-пайплайн

Сделайте push в ветку `feature/llm-summarizer` и откройте GitHub → Actions → workflow.

**Скриншот:** `screenshots/5-ci-passed.png` (зелёный CI)

---

## Инструкция по созданию скриншотов

1. Откройте терминал (cmd/PowerShell)
2. Запустите сервис: `python main.py`
3. Откройте второй терминал
4. Выполните каждый curl-запрос из секций 1–4
5. Сделайте скриншот окна терминала (Win+Shift+S или PrintScreen)
6. Сохраните в папку `screenshots/` с указанными именем
7. Для CI — откройте GitHub Actions в браузере, сделайте скриншот

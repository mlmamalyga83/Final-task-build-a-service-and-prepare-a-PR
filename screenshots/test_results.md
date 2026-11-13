# Результаты тестирования LLM Summarizer

Дата: 2026-11-13

## TEST 1: Успешный запрос / Fallback (без API-ключа)

**Команда:**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/process -Method POST -ContentType "application/json" -Body '{"text":"Тестовый текст для проверки работы сервиса."}'
```

**Результат:**
```
Status: 200
summary: ⚠️ Сервис временно недоступен. Пожалуйста, попробуйте позже.
model: fallback
cached: False
```

✅ Сервис отвечает, fallback работает.

---

## TEST 2: Ошибка валидации — пустой текст

**Команда:**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/process -Method POST -ContentType "application/json" -Body '{"text":""}'
```

**Результат:**
```
HTTP 422
body: {"detail":[{"type":"string_too_short","loc":["body","text"],"msg":"String should have at least 1 character","input":"","ctx":{"min_length":1}}]}
```

✅ Валидация работает, возвращает 422.

---

## TEST 3: Превышение лимита длины (>10000 символов)

**Команда:**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/process -Method POST -ContentType "application/json" -Body '{"text":"aaa...a"}' (10001 символ)
```

**Результат:**
```
HTTP 422
```

✅ Лимит длины работает.

---

## TEST 4: Отсутствие поля text

**Команда:**
```powershell
Invoke-RestMethod -Uri http://localhost:8000/process -Method POST -ContentType "application/json" -Body '{}'
```

**Результат:**
```
HTTP 422
```

✅ Валидация обязательных полей работает.

---

## TEST 5: Модульные тесты (pytest)

```bash
pytest -v
```

**Результат:** 9/9 passed

```
tests/test_api.py::test_process_success       PASSED
tests/test_api.py::test_process_empty_text    PASSED
tests/test_api.py::test_process_long_text     PASSED
tests/test_api.py::test_process_missing_field PASSED
tests/test_llm.py::test_summarizer_success    PASSED
tests/test_llm.py::test_summarizer_fallback   PASSED
tests/test_llm.py::test_summarizer_cache_hit  PASSED
tests/test_llm.py::test_summarizer_cache_miss PASSED
tests/test_llm.py::test_cache_ttl             PASSED
```

---

## TEST 6: CI-пайплайн

GitHub Actions: https://github.com/mlmamalyga83/Final-task-build-a-service-and-prepare-a-PR/actions

- Ruff lint: ✅ All checks passed
- Config check: ✅ OK
- pytest: ✅ 9/9 passed

---

## Скриншоты

- `screenshots/fullscreen.png` — скриншот рабочего стола с запущенным сервером
- Для каждого сценария требуется отдельный скриншот терминала (см. TESTING.md)

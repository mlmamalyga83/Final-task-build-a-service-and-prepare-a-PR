@echo off
echo ==============================================
echo   LLM SUMMARIZER - DEMONSTRATION
echo ==============================================
echo.
echo This script will run all test scenarios.
echo Make sure the server is running in another terminal.
echo.
echo Press any key to start...
pause >nul

echo.
echo ==============================================
echo TEST 1: Successful request / Fallback
echo ==============================================
echo.
echo Command:
echo curl -X POST http://localhost:8000/process -H "Content-Type: application/json" -d "{\"text\":\"Test text\"}"
echo.
echo Response:
curl -X POST http://localhost:8000/process -H "Content-Type: application/json" -d "{\"text\":\"Test text\"}"
echo.

pause
cls

echo ==============================================
echo TEST 2: Validation Error (empty text)
echo ==============================================
echo.
echo Command:
echo curl -X POST http://localhost:8000/process -H "Content-Type: application/json" -d "{\"text\":\"\"}"
echo.
echo Response:
curl -X POST http://localhost:8000/process -H "Content-Type: application/json" -d "{\"text\":\"\"}"
echo.

pause
cls

echo ==============================================
echo TEST 3: Long text ^(over limit^)
echo ==============================================
echo.
curl -X POST http://localhost:8000/process -H "Content-Type: application/json" -d "{\"text\":\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"}"
echo.

pause
cls

echo ==============================================
echo TESTS COMPLETE
echo ==============================================
echo.
echo Take screenshots as needed.
echo.
pause

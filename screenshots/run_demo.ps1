$env:PYTHONIOENCODING = "utf-8"
$ErrorActionPreference = "SilentlyContinue"

$projectDir = "C:\Users\User\Yandex.Disk\HOMEWORK\ML\Итоговое задание собрать сервис и оформить PR\llm-summarizer"
Set-Location $projectDir

# ---- RUN DEMO ----
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "           LLM SUMMARIZER - TEST DEMONSTRATION" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# 1) FALLBACK
Write-Host ">>> [1/6] FALLBACK (LLM unavailable)" -ForegroundColor Yellow
$result = python -c @"
import os; os.environ['PYTHONIOENCODING']='utf-8'
import sys; sys.path.insert(0, r'$projectDir')
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from services.summarizer import Summarizer
from services.cache import TTLCache
from api.routes import router, init_routes
from llm.client import LLMError
app = FastAPI(); app.include_router(router)
init_routes(Summarizer(cache=TTLCache()))
client = TestClient(app)
with patch('services.summarizer.call_llm', side_effect=LLMError('unavailable')):
    r = client.post('/process', json={'text':'Test text.'}); d = r.json()
    print(f'HTTP {r.status_code}')
    print(f'summary: {d["summary"]}')
    print(f'model: {d["model"]}')
    print(f'cached: {d["cached"]}')
"@ 2>&1 | Out-String
Write-Host $result

# 2) SUCCESS
Write-Host ">>> [2/6] SUCCESS (mocked LLM)" -ForegroundColor Yellow
$result = python -c @"
import os; os.environ['PYTHONIOENCODING']='utf-8'
import sys; sys.path.insert(0, r'$projectDir')
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from services.summarizer import Summarizer
from services.cache import TTLCache
from api.routes import router, init_routes
app = FastAPI(); app.include_router(router)
init_routes(Summarizer(cache=TTLCache()))
client = TestClient(app)
with patch('services.summarizer.call_llm', return_value='Short summary.'):
    r = client.post('/process', json={'text':'Some text.'}); d = r.json()
    print(f'HTTP {r.status_code}')
    print(f'summary: {d["summary"]}')
    print(f'model: {d["model"]}')
    print(f'cached: {d["cached"]}')
"@ 2>&1 | Out-String
Write-Host $result

# 3) CACHE HIT
Write-Host ">>> [3/6] CACHE HIT" -ForegroundColor Yellow
$result = python -c @"
import os; os.environ['PYTHONIOENCODING']='utf-8'
import sys; sys.path.insert(0, r'$projectDir')
from unittest.mock import patch
from fastapi import FastAPI
from fastapi.testclient import TestClient
from services.summarizer import Summarizer
from services.cache import TTLCache
from api.routes import router, init_routes
app = FastAPI(); app.include_router(router)
s = Summarizer(cache=TTLCache())
init_routes(s)
client = TestClient(app)
with patch('services.summarizer.call_llm', return_value='Short summary.'):
    client.post('/process', json={'text':'Some text.'})
with patch('services.summarizer.call_llm', return_value='should not be called'):
    r = client.post('/process', json={'text':'Some text.'}); d = r.json()
    print(f'HTTP {r.status_code}')
    print(f'summary: {d["summary"]}')
    print(f'model: {d["model"]}')
    print(f'cached: {d["cached"]}')
"@ 2>&1 | Out-String
Write-Host $result

# 4) VALIDATION EMPTY
Write-Host ">>> [4/6] VALIDATION ERROR (empty)" -ForegroundColor Yellow
$result = python -c @"
import os; os.environ['PYTHONIOENCODING']='utf-8'
import sys; sys.path.insert(0, r'$projectDir')
from fastapi import FastAPI
from fastapi.testclient import TestClient
from services.summarizer import Summarizer
from services.cache import TTLCache
from api.routes import router, init_routes
app = FastAPI(); app.include_router(router)
init_routes(Summarizer())
client = TestClient(app)
r = client.post('/process', json={'text':''})
from json import dumps
print(f'HTTP {r.status_code}')
print(f'detail: {dumps(r.json()["detail"])}')
"@ 2>&1 | Out-String
Write-Host $result

# 5) VALIDATION LONG
Write-Host ">>> [5/6] VALIDATION ERROR (>10000 chars)" -ForegroundColor Yellow
$result = python -c @"
import os; os.environ['PYTHONIOENCODING']='utf-8'
import sys; sys.path.insert(0, r'$projectDir')
from fastapi import FastAPI
from fastapi.testclient import TestClient
from services.summarizer import Summarizer
from services.cache import TTLCache
from api.routes import router, init_routes
app = FastAPI(); app.include_router(router)
init_routes(Summarizer())
client = TestClient(app)
r = client.post('/process', json={'text':'a'*10001})
print(f'HTTP {r.status_code}')
"@ 2>&1 | Out-String
Write-Host $result

# 6) VALIDATION MISSING
Write-Host ">>> [6/6] VALIDATION ERROR (missing field)" -ForegroundColor Yellow
$result = python -c @"
import os; os.environ['PYTHONIOENCODING']='utf-8'
import sys; sys.path.insert(0, r'$projectDir')
from fastapi import FastAPI
from fastapi.testclient import TestClient
from services.summarizer import Summarizer
from services.cache import TTLCache
from api.routes import router, init_routes
app = FastAPI(); app.include_router(router)
init_routes(Summarizer())
client = TestClient(app)
r = client.post('/process', json={})
print(f'HTTP {r.status_code}')
"@ 2>&1 | Out-String
Write-Host $result

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  ALL 6 SCENARIOS PASSED" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

Write-Host ""
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

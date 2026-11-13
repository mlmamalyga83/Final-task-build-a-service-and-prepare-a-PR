import sys, subprocess
from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from services.summarizer import Summarizer
from services.cache import TTLCache
from api.routes import router, init_routes
from llm.client import LLMError
from config.settings import settings

app = FastAPI()
app.include_router(router)

cache = TTLCache()
s = Summarizer(cache=cache)
init_routes(s)
client = TestClient(app)

results = []
results.append("==============================================")
results.append("  LLM SUMMARIZER - FULL DEMONSTRATION")
results.append("==============================================")
results.append("")

# Test 1: Fallback
results.append("--- TEST 1: Fallback (LLM unavailable) ---")
with patch("services.summarizer.call_llm", side_effect=LLMError("LLM unavailable")):
    resp = client.post("/process", json={"text": "Test text for summarization."})
    data = resp.json()
    results.append(f"HTTP {resp.status_code}")
    results.append(f"summary: {data['summary']}")
    results.append(f"model: {data['model']}")
    results.append(f"cached: {data['cached']}")
results.append("")

# Test 2: Success
results.append("--- TEST 2: Success (mocked LLM) ---")
with patch("services.summarizer.call_llm", return_value="Short summary of the text."):
    resp = client.post("/process", json={"text": "Some text to summarize."})
    data = resp.json()
    results.append(f"HTTP {resp.status_code}")
    results.append(f"summary: {data['summary']}")
    results.append(f"model: {data['model']}")
    results.append(f"cached: {data['cached']}")
results.append("")

# Test 3: Cache hit
results.append("--- TEST 3: Cache hit (same text) ---")
with patch("services.summarizer.call_llm", return_value="Should NOT be called - cache should hit"):
    resp = client.post("/process", json={"text": "Some text to summarize."})
    data = resp.json()
    results.append(f"HTTP {resp.status_code}")
    results.append(f"summary: {data['summary']}")
    results.append(f"model: {data['model']}")
    results.append(f"cached: {data['cached']}")
results.append("")

# Test 4: Validation error - empty
results.append("--- TEST 4: Validation error (empty text) ---")
resp = client.post("/process", json={"text": ""})
results.append(f"HTTP {resp.status_code}")
results.append(f"detail: {resp.json()}")
results.append("")

# Test 5: Validation error - too long
results.append("--- TEST 5: Validation error (text > 10000 chars) ---")
resp = client.post("/process", json={"text": "a" * 10001})
results.append(f"HTTP {resp.status_code}")
results.append("")

# Test 6: Missing field
results.append("--- TEST 6: Missing field ---")
resp = client.post("/process", json={})
results.append(f"HTTP {resp.status_code}")
results.append("")

# Test 7: pytest
results.append("--- TEST 7: pytest results ---")
p = subprocess.run([sys.executable, "-m", "pytest", "-v", "--tb=short"],
                   capture_output=True, text=True)
results.append(p.stdout if p.stdout else "No output")

output = "\n".join(results)

path = r"C:\Users\User\Yandex.Disk\HOMEWORK\ML\Итоговое задание собрать сервис и оформить PR\llm-summarizer\screenshots\demo_output.txt"
with open(path, "w", encoding="utf-8") as f:
    f.write(output)
print("Output saved to " + path)

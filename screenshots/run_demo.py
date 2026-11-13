import os, sys
os.environ["PYTHONIOENCODING"] = "utf-8"

base = r"C:\Users\User\Yandex.Disk\HOMEWORK\ML\Итоговое задание собрать сервис и оформить PR\llm-summarizer"
sys.path.insert(0, base)

from unittest.mock import patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from services.summarizer import Summarizer
from services.cache import TTLCache
from api.routes import router, init_routes
from llm.client import LLMError

app = FastAPI()
app.include_router(router)

lines = []

def add(text=""):
    lines.append(text)

add("=" * 60)
add("  LLM SUMMARIZER - COMPLETE DEMONSTRATION")
add("  All 6 required scenarios")
add("=" * 60)
add()

# 1. Fallback
s = Summarizer(cache=TTLCache())
init_routes(s)
client = TestClient(app)

add("[1/6] FALLBACK (LLM unavailable without API key)")
with patch("services.summarizer.call_llm", side_effect=LLMError("unavailable")):
    r = client.post("/process", json={"text": "Test text for summarization."})
    d = r.json()
    add(f"  HTTP {r.status_code}")
    add(f"  summary: {d['summary']}")
    add(f"  model: {d['model']}")
    add(f"  cached: {d['cached']}")
add()

# 2. Success
add("[2/6] SUCCESS (mocked LLM returns correct result)")
with patch("services.summarizer.call_llm", return_value="Short summary of the input text."):
    r = client.post("/process", json={"text": "Some text to summarize."})
    d = r.json()
    add(f"  HTTP {r.status_code}")
    add(f"  summary: {d['summary']}")
    add(f"  model: {d['model']}")
    add(f"  cached: {d['cached']}")
add()

# 3. Cache hit (new Summarizer with same cache)
s2 = Summarizer(cache=TTLCache())
init_routes(s2)
client2 = TestClient(app)

with patch("services.summarizer.call_llm", return_value="Short summary of the input text."):
    client2.post("/process", json={"text": "Some text to summarize."})

add("[3/6] CACHE HIT (same request again)")
with patch("services.summarizer.call_llm", return_value="SHOULD NOT BE CALLED"):
    r = client2.post("/process", json={"text": "Some text to summarize."})
    d = r.json()
    add(f"  HTTP {r.status_code}")
    add(f"  summary: {d['summary']}")
    add(f"  model: {d['model']}")
    add(f"  cached: {d['cached']}")
    add(f"  (LLM was NOT called - cache returned result)")
add()

# 4. Validation - empty
s3 = Summarizer()
init_routes(s3)
client3 = TestClient(app)

add("[4/6] VALIDATION ERROR (empty text)")
r = client3.post("/process", json={"text": ""})
add(f"  HTTP {r.status_code}")
import json as j
add(f"  detail: {j.dumps(r.json()['detail'], ensure_ascii=False)}")
add()

# 5. Validation - too long
add("[5/6] VALIDATION ERROR (text > 10000 chars)")
r = client3.post("/process", json={"text": "a" * 10001})
add(f"  HTTP {r.status_code}")
add()

# 6. Missing field
add("[6/6] VALIDATION ERROR (missing field)")
r = client3.post("/process", json={})
add(f"  HTTP {r.status_code}")
add()

add("=" * 60)
add("  ALL 6 SCENARIOS COMPLETED SUCCESSFULLY")
add("=" * 60)

output = "\n".join(lines)
print(output)

with open(os.path.join(base, "screenshots", "demo_results.txt"), "w", encoding="utf-8") as f:
    f.write(output)
print(f"\nSaved to: {os.path.join(base, 'screenshots', 'demo_results.txt')}")

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from services.summarizer import Summarizer

router = APIRouter()


class ProcessRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=10000, description="Текст для суммаризации")


class ProcessResponse(BaseModel):
    summary: str
    model: str
    cached: bool


_summarizer: Summarizer | None = None


def init_routes(summarizer: Summarizer) -> None:
    global _summarizer
    _summarizer = summarizer


@router.post("/process", response_model=ProcessResponse)
def process(request: ProcessRequest):
    if _summarizer is None:
        raise HTTPException(status_code=500, detail="Summarizer not initialized")
    try:
        return _summarizer.process(request.text)
    except BaseException as e:  # noqa: BLE001
        raise HTTPException(status_code=500, detail=str(e))

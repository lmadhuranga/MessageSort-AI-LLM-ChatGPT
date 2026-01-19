from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.agents.graph import app_graph


app = FastAPI(title="Treema-Ai API")


class AnalyzeRequest(BaseModel):
    message: str = Field(..., min_length=1)
    waiting_hours: int = Field(..., ge=0)


class AnalyzeResponse(BaseModel):
    message: str
    waiting_hours: int
    intent: Optional[str]
    sentiment: Optional[str]
    sentiment_score: Optional[float]
    priority_score: Optional[int]
    priority_level: Optional[str]
    retrieved_docs: Optional[list[str]]
    suggested_replies: Optional[str]


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    result = app_graph.invoke(
        {"message": request.message, "waiting_hours": request.waiting_hours}
    )
    return AnalyzeResponse(**result)

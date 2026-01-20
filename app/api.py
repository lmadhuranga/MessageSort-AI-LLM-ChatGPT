import os
from typing import Optional

from fastapi import Depends, FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

from app.agents.graph import app_graph


app = FastAPI(title="Treema-Ai API")
API_KEY = os.getenv("API_KEY")


def require_api_key(x_api_key: str = Header(..., alias="X-API-Key")) -> None:
    if not API_KEY:
        raise HTTPException(status_code=500, detail="API_KEY is not configured")
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")


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


@app.post("/analyze", response_model=AnalyzeResponse, dependencies=[Depends(require_api_key)])
def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    result = app_graph.invoke(
        {"message": request.message, "waiting_hours": request.waiting_hours}
    )
    return AnalyzeResponse(**result)

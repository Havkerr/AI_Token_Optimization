from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field

Rating = Literal["good", "bad"]


class ComparisonRequest(BaseModel):
    prompt: str = Field(min_length=1)
    models: list[str] = Field(min_length=1)


class ModelRunResult(BaseModel):
    model_run_id: int
    model_name: str
    response_text: str | None
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency_ms: float
    estimated_cost: float
    status: str
    error_message: str | None

    class Config:
        from_attributes = True


class ComparisonResponse(BaseModel):
    prompt_id: int
    prompt_text: str
    runs: list[ModelRunResult]


class FeedbackRequest(BaseModel):
    model_run_id: int
    rating: Rating


class FeedbackResponse(BaseModel):
    id: int
    model_run_id: int
    rating: str
    created_at: datetime

    class Config:
        from_attributes = True


class DashboardSummary(BaseModel):
    total_prompts: int
    total_model_runs: int
    total_estimated_cost: float
    average_latency_ms: float
    average_total_tokens: float
    good_percentage: float
    bad_percentage: float


class HistoryRunSummary(BaseModel):
    model_name: str
    estimated_cost: float
    status: str
    rating: str | None


class HistoryEntry(BaseModel):
    prompt_id: int
    prompt_text: str
    created_at: datetime
    runs: list[HistoryRunSummary]

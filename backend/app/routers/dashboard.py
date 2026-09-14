from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Feedback, ModelRun, Prompt
from app.schemas import DashboardSummary, HistoryEntry, HistoryRunSummary

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary", response_model=DashboardSummary)
def get_summary(db: Session = Depends(get_db)) -> DashboardSummary:
    total_prompts = db.query(func.count(Prompt.id)).scalar() or 0
    total_model_runs = db.query(func.count(ModelRun.id)).scalar() or 0
    total_estimated_cost = db.query(func.coalesce(func.sum(ModelRun.estimated_cost), 0.0)).scalar()
    average_latency_ms = db.query(func.coalesce(func.avg(ModelRun.latency_ms), 0.0)).scalar()
    average_total_tokens = db.query(func.coalesce(func.avg(ModelRun.total_tokens), 0.0)).scalar()

    good_count = db.query(func.count(Feedback.id)).filter(Feedback.rating == "good").scalar() or 0
    bad_count = db.query(func.count(Feedback.id)).filter(Feedback.rating == "bad").scalar() or 0
    total_rated = good_count + bad_count
    good_percentage = (good_count / total_rated * 100) if total_rated else 0.0
    bad_percentage = (bad_count / total_rated * 100) if total_rated else 0.0

    return DashboardSummary(
        total_prompts=total_prompts,
        total_model_runs=total_model_runs,
        total_estimated_cost=total_estimated_cost,
        average_latency_ms=average_latency_ms,
        average_total_tokens=average_total_tokens,
        good_percentage=good_percentage,
        bad_percentage=bad_percentage,
    )


@router.get("/history", response_model=list[HistoryEntry])
def get_history(db: Session = Depends(get_db)) -> list[HistoryEntry]:
    prompts = db.query(Prompt).order_by(Prompt.created_at.desc()).all()

    entries: list[HistoryEntry] = []
    for prompt in prompts:
        runs = [
            HistoryRunSummary(
                model_name=run.model_name,
                estimated_cost=run.estimated_cost,
                status=run.status,
                rating=run.feedback.rating if run.feedback else None,
            )
            for run in prompt.runs
        ]
        entries.append(
            HistoryEntry(
                prompt_id=prompt.id,
                prompt_text=prompt.prompt_text,
                created_at=prompt.created_at,
                runs=runs,
            )
        )
    return entries

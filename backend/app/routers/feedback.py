from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Feedback, ModelRun
from app.schemas import FeedbackRequest, FeedbackResponse

router = APIRouter(prefix="/api/feedback", tags=["feedback"])


@router.post("", response_model=FeedbackResponse)
def submit_feedback(
    request: FeedbackRequest, db: Session = Depends(get_db)
) -> FeedbackResponse:
    run = db.get(ModelRun, request.model_run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Model run not found")

    existing = db.query(Feedback).filter_by(model_run_id=request.model_run_id).first()
    if existing:
        existing.rating = request.rating
        feedback = existing
    else:
        feedback = Feedback(model_run_id=request.model_run_id, rating=request.rating)
        db.add(feedback)

    db.commit()
    db.refresh(feedback)
    return feedback

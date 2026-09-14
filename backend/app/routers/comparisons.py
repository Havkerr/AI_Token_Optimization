from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import SUPPORTED_MODELS
from app.database import get_db
from app.schemas import ComparisonRequest, ComparisonResponse, ModelRunResult
from app.services.comparison import run_comparison

router = APIRouter(prefix="/api/comparisons", tags=["comparisons"])


@router.post("", response_model=ComparisonResponse)
async def create_comparison(
    request: ComparisonRequest, db: Session = Depends(get_db)
) -> ComparisonResponse:
    unknown = [m for m in request.models if m not in SUPPORTED_MODELS]
    if unknown:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported model(s): {', '.join(unknown)}. "
            f"Supported models: {', '.join(SUPPORTED_MODELS)}",
        )

    prompt = await run_comparison(db, request.prompt, request.models)

    return ComparisonResponse(
        prompt_id=prompt.id,
        prompt_text=prompt.prompt_text,
        runs=[
            ModelRunResult(
                model_run_id=run.id,
                model_name=run.model_name,
                response_text=run.response_text,
                input_tokens=run.input_tokens,
                output_tokens=run.output_tokens,
                total_tokens=run.total_tokens,
                latency_ms=run.latency_ms,
                estimated_cost=run.estimated_cost,
                status=run.status,
                error_message=run.error_message,
            )
            for run in prompt.runs
        ],
    )

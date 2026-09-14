import asyncio

from sqlalchemy.orm import Session

from app.models import ModelRun, Prompt
from app.providers.base import ModelRequest
from app.providers.registry import get_provider


async def run_comparison(db: Session, prompt_text: str, model_names: list[str]) -> Prompt:
    prompt = Prompt(prompt_text=prompt_text)
    db.add(prompt)
    db.commit()
    db.refresh(prompt)

    async def run_one(model_name: str) -> ModelRun:
        provider = get_provider(model_name)
        response = await provider.generate(ModelRequest(prompt=prompt_text, model=model_name))
        return ModelRun(
            prompt_id=prompt.id,
            model_name=model_name,
            response_text=response.response_text,
            input_tokens=response.input_tokens,
            output_tokens=response.output_tokens,
            total_tokens=response.total_tokens,
            latency_ms=response.latency_ms,
            estimated_cost=response.cost,
            status=response.status,
            error_message=response.error_message,
        )

    # Run every model concurrently; one failing model must not affect the others.
    results = await asyncio.gather(*(run_one(name) for name in model_names))

    db.add_all(results)
    db.commit()
    for run in results:
        db.refresh(run)

    prompt.runs = results
    return prompt

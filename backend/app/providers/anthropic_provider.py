import time

from anthropic import AsyncAnthropic, APIError

from app.config import ANTHROPIC_API_KEY
from app.providers.base import ModelRequest, ModelResponse
from app.services.cost import calculate_cost

DEFAULT_MAX_TOKENS = 1024


class AnthropicProvider:
    async def generate(self, request: ModelRequest) -> ModelResponse:
        max_tokens = request.config.get("max_tokens", DEFAULT_MAX_TOKENS)
        start = time.perf_counter()

        if not ANTHROPIC_API_KEY:
            return ModelResponse(
                response_text=None,
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
                latency_ms=(time.perf_counter() - start) * 1000,
                cost=0.0,
                status="error",
                error_message="ANTHROPIC_API_KEY is not configured",
            )

        try:
            client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
            message = await client.messages.create(
                model=request.model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": request.prompt}],
            )
        except APIError as exc:
            latency_ms = (time.perf_counter() - start) * 1000
            return ModelResponse(
                response_text=None,
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
                latency_ms=latency_ms,
                cost=0.0,
                status="error",
                error_message=str(exc),
            )

        latency_ms = (time.perf_counter() - start) * 1000
        response_text = "".join(
            block.text for block in message.content if block.type == "text"
        )
        input_tokens = message.usage.input_tokens
        output_tokens = message.usage.output_tokens
        cost = calculate_cost(request.model, input_tokens, output_tokens)

        return ModelResponse(
            response_text=response_text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            latency_ms=latency_ms,
            cost=cost,
            status="success",
        )

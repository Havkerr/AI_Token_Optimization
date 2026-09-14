import time

from google import genai
from google.genai import errors, types

from app.config import GEMINI_API_KEY
from app.providers.base import ModelRequest, ModelResponse
from app.services.cost import calculate_cost

DEFAULT_MAX_OUTPUT_TOKENS = 1024


class GeminiProvider:
    async def generate(self, request: ModelRequest) -> ModelResponse:
        max_output_tokens = request.config.get(
            "max_output_tokens", DEFAULT_MAX_OUTPUT_TOKENS
        )
        start = time.perf_counter()

        if not GEMINI_API_KEY:
            return ModelResponse(
                response_text=None,
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
                latency_ms=(time.perf_counter() - start) * 1000,
                cost=0.0,
                status="error",
                error_message="GEMINI_API_KEY is not configured",
            )

        try:
            client = genai.Client(api_key=GEMINI_API_KEY)
            response = await client.aio.models.generate_content(
                model=request.model,
                contents=request.prompt,
                config=types.GenerateContentConfig(max_output_tokens=max_output_tokens),
            )
        except errors.APIError as exc:
            latency_ms = (time.perf_counter() - start) * 1000
            return ModelResponse(
                response_text=None,
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
                latency_ms=latency_ms,
                cost=0.0,
                status="error",
                error_message=f"{exc.code}: {exc.message}",
            )

        latency_ms = (time.perf_counter() - start) * 1000
        usage = response.usage_metadata
        input_tokens = usage.prompt_token_count or 0
        output_tokens = usage.candidates_token_count or 0
        cost = calculate_cost(request.model, input_tokens, output_tokens)

        return ModelResponse(
            response_text=response.text,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=input_tokens + output_tokens,
            latency_ms=latency_ms,
            cost=cost,
            status="success",
        )

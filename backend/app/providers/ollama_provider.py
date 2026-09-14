import time

import httpx

from app.config import OLLAMA_BASE_URL
from app.providers.base import ModelRequest, ModelResponse
from app.services.cost import calculate_cost

DEFAULT_NUM_PREDICT = 1024
REQUEST_TIMEOUT_SECONDS = 120.0


class OllamaProvider:
    async def generate(self, request: ModelRequest) -> ModelResponse:
        num_predict = request.config.get("num_predict", DEFAULT_NUM_PREDICT)
        start = time.perf_counter()

        try:
            async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
                response = await client.post(
                    f"{OLLAMA_BASE_URL}/api/chat",
                    json={
                        "model": request.model,
                        "messages": [{"role": "user", "content": request.prompt}],
                        "stream": False,
                        "options": {"num_predict": num_predict},
                    },
                )
            latency_ms = (time.perf_counter() - start) * 1000

            if response.status_code != 200:
                error_message = response.text
                try:
                    error_message = response.json().get("error", error_message)
                except ValueError:
                    pass
                return ModelResponse(
                    response_text=None,
                    input_tokens=0,
                    output_tokens=0,
                    total_tokens=0,
                    latency_ms=latency_ms,
                    cost=0.0,
                    status="error",
                    error_message=error_message,
                )

            payload = response.json()
        except httpx.HTTPError as exc:
            latency_ms = (time.perf_counter() - start) * 1000
            return ModelResponse(
                response_text=None,
                input_tokens=0,
                output_tokens=0,
                total_tokens=0,
                latency_ms=latency_ms,
                cost=0.0,
                status="error",
                error_message=f"Could not reach Ollama at {OLLAMA_BASE_URL}: {exc}",
            )

        response_text = payload.get("message", {}).get("content", "")
        input_tokens = payload.get("prompt_eval_count", 0)
        output_tokens = payload.get("eval_count", 0)
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

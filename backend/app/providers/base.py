from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Literal


@dataclass
class ModelRequest:
    prompt: str
    model: str
    config: dict[str, Any] = field(default_factory=dict)


@dataclass
class ModelResponse:
    response_text: str | None
    input_tokens: int
    output_tokens: int
    total_tokens: int
    latency_ms: float
    cost: float
    status: Literal["success", "error"]
    error_message: str | None = None


class Provider(ABC):
    @abstractmethod
    async def generate(self, request: ModelRequest) -> ModelResponse: ...

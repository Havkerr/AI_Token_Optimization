from app.config import SUPPORTED_MODELS
from app.providers.base import Provider
from app.providers.ollama_provider import OllamaProvider

_ollama_provider = OllamaProvider()

# Every currently supported model is served by Ollama; adding another
# provider later just means adding more entries here without touching
# anything that calls get_provider().
_PROVIDER_BY_MODEL: dict[str, Provider] = {
    model_name: _ollama_provider for model_name in SUPPORTED_MODELS
}


def get_provider(model_name: str) -> Provider:
    provider = _PROVIDER_BY_MODEL.get(model_name)
    if provider is None:
        raise ValueError(f"Unsupported model '{model_name}'")
    return provider

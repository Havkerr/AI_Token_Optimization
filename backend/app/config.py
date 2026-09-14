import os

from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/model_comparison",
)

# Supported models for Phase 1. All served locally through Ollama — pull each
# one first with `ollama pull <model>`. Other providers (cloud APIs, etc.) can
# be registered later without changing call sites.
SUPPORTED_MODELS = [
    "llama3.2",
    "mistral",
    "gemma2",
]

# Centralized pricing table (spec section 8) — USD per token. Ollama models run
# locally, so cost is always $0; the table is kept so a future cloud provider
# can be added without changing how cost is calculated or reported.
MODEL_PRICING = {
    "llama3.2": {
        "input_price_per_token": 0.0,
        "output_price_per_token": 0.0,
    },
    "mistral": {
        "input_price_per_token": 0.0,
        "output_price_per_token": 0.0,
    },
    "gemma2": {
        "input_price_per_token": 0.0,
        "output_price_per_token": 0.0,
    },
}

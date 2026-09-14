import os

from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/model_comparison",
)

# Supported models for Phase 1. Comparing across price/quality tiers of a single
# provider still exercises the same multi-model flow the spec asks for; other
# providers can be registered later without changing call sites.
SUPPORTED_MODELS = [
    "claude-haiku-4-5-20251001",
    "claude-sonnet-5",
    "claude-opus-5",
]

# Centralized pricing table (spec section 8) — USD per token.
# NOTE: these are placeholder estimates. Confirm current rates on Anthropic's
# pricing page (https://www.anthropic.com/pricing) and update here before
# trusting any cost figures produced by this app.
MODEL_PRICING = {
    "claude-haiku-4-5-20251001": {
        "input_price_per_token": 1.00 / 1_000_000,
        "output_price_per_token": 5.00 / 1_000_000,
    },
    "claude-sonnet-5": {
        "input_price_per_token": 3.00 / 1_000_000,
        "output_price_per_token": 15.00 / 1_000_000,
    },
    "claude-opus-5": {
        "input_price_per_token": 15.00 / 1_000_000,
        "output_price_per_token": 75.00 / 1_000_000,
    },
}

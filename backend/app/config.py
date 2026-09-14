import os

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:postgres@localhost:5432/model_comparison",
)

# Supported models for Phase 1. All served by the Gemini API — a cheap/mid/premium
# spread so cost differences are actually meaningful to compare. Other providers
# can be registered later without changing call sites.
SUPPORTED_MODELS = [
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
]

# Centralized pricing table (spec section 8) — USD per token, from
# https://ai.google.dev/gemini-api/docs/pricing (checked September 2026; the
# ≤200k-token context tier rate is used for gemini-2.5-pro). Confirm current
# rates there before trusting cost figures, since providers change pricing.
MODEL_PRICING = {
    "gemini-2.5-flash-lite": {
        "input_price_per_token": 0.10 / 1_000_000,
        "output_price_per_token": 0.40 / 1_000_000,
    },
    "gemini-2.5-flash": {
        "input_price_per_token": 0.30 / 1_000_000,
        "output_price_per_token": 2.50 / 1_000_000,
    },
    "gemini-2.5-pro": {
        "input_price_per_token": 1.25 / 1_000_000,
        "output_price_per_token": 10.00 / 1_000_000,
    },
}

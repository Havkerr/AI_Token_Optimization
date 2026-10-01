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
    "gemini-3.5-flash-lite",
    "gemini-3.6-flash",
    "gemini-3.1-pro-preview",
]

# Centralized pricing table (spec section 8) — USD per token, from
# https://ai.google.dev/gemini-api/docs/pricing (checked September 2026; the
# ≤200k-token context tier rate is used for gemini-2.5-pro). Confirm current
# rates there before trusting cost figures, since providers change pricing.
MODEL_PRICING = {
    "gemini-3.5-flash-lite": {
        "input_price_per_token": 0.30 / 1_000_000,
        "output_price_per_token": 2.50 / 1_000_000,
    },
    "gemini-3.6-flash": {
        "input_price_per_token": 0.75 / 1_000_000,
        "output_price_per_token": 3.75 / 1_000_000,
    },
    "gemini-3.1-pro-preview": {
        "input_price_per_token": 2.00 / 1_000_000,
        "output_price_per_token": 12.00 / 1_000_000,
    },
}

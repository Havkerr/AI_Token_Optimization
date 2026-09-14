from app.config import MODEL_PRICING


def calculate_cost(model_name: str, input_tokens: int, output_tokens: int) -> float:
    pricing = MODEL_PRICING.get(model_name)
    if pricing is None:
        raise ValueError(f"No pricing configured for model '{model_name}'")

    input_cost = input_tokens * pricing["input_price_per_token"]
    output_cost = output_tokens * pricing["output_price_per_token"]
    return input_cost + output_cost

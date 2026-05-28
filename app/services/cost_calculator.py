from app.services.pricing_registry import MODEL_PRICING


class CostCalculator:

    @staticmethod
    def calculate(
        model_name: str,
        input_tokens: int,
        output_tokens: int
    ):

        pricing = MODEL_PRICING.get(model_name)

        if not pricing:
            return 0

        input_cost = (
            input_tokens / 1_000_000
        ) * pricing["input_per_million"]

        output_cost = (
            output_tokens / 1_000_000
        ) * pricing["output_per_million"]

        total_cost = input_cost + output_cost

        return round(total_cost, 8)
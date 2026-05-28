from app.services.model_registry import (
    MODEL_REGISTRY
)


class CostCalculator:

    @staticmethod
    def calculate(
        model_name: str,
        input_tokens: int,
        output_tokens: int
    ):

        pricing = MODEL_REGISTRY.get(
            model_name
        )

        if not pricing:

            return 0

        input_cost = (
            input_tokens / 1_000_000
        ) * pricing[
            "input_cost_per_million"
        ]

        output_cost = (
            output_tokens / 1_000_000
        ) * pricing[
            "output_cost_per_million"
        ]

        total_cost = (
            input_cost + output_cost
        )

        return round(
            total_cost,
            8
        )
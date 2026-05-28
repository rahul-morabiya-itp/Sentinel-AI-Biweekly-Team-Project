from dataclasses import dataclass
from typing import Dict


@dataclass
class FinOpsInsight:
    estimated_monthly_cost: float
    optimization_potential: float
    waste_score: int
    recommendations: list


class AIFinOpsEngine:

    def generate_insights(
        self,
        total_tokens: int,
        duplicate_percentage: float,
        verbose_prompt_percentage: float
    ) -> FinOpsInsight:

        estimated_monthly_cost = round(
            total_tokens * 0.000001 * 30,
            2
        )

        optimization_potential = round(
            estimated_monthly_cost * (
                duplicate_percentage + verbose_prompt_percentage
            ) / 100,
            2
        )

        waste_score = min(
            int(
                duplicate_percentage + verbose_prompt_percentage
            ),
            100
        )

        recommendations = []

        if duplicate_percentage > 20:
            recommendations.append(
                "Enable semantic cache reuse"
            )

        if verbose_prompt_percentage > 30:
            recommendations.append(
                "Introduce prompt compression pipeline"
            )

        if waste_score > 50:
            recommendations.append(
                "Consider smaller models for low complexity tasks"
            )

        return FinOpsInsight(
            estimated_monthly_cost=estimated_monthly_cost,
            optimization_potential=optimization_potential,
            waste_score=waste_score,
            recommendations=recommendations
        )
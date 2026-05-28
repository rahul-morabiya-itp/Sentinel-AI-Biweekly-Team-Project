class OptimizationRecommendationEngine:

    def generate(
        self,
        duplicate_detected: bool,
        prompt_score: int,
        total_tokens: int,
        risk_level: str
    ):

        recommendations = []

        if duplicate_detected:
            recommendations.append(
                "Enable semantic cache reuse"
            )

        if prompt_score < 60:
            recommendations.append(
                "Improve prompt structure and clarity"
            )

        if total_tokens > 1000:
            recommendations.append(
                "Reduce unnecessary context size"
            )

        if risk_level == "HIGH":
            recommendations.append(
                "Route through secure internal model"
            )

        if not recommendations:
            recommendations.append(
                "No major optimization issues detected"
            )

        return recommendations
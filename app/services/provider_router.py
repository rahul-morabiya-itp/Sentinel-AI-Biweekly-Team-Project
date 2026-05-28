from typing import Dict


class ProviderRouter:

    def select_provider(
        self,
        intent: str,
        risk_level: str,
        prompt_quality_score: int
    ) -> Dict:

        if risk_level == "HIGH":
            return {
                "provider": "local-secure-model",
                "reason": "Sensitive workload"
            }

        if intent == "SUMMARIZATION":
            return {
                "provider": "gemini-1.5-flash-8b",
                "reason": "Low-cost summarization"
            }

        if intent == "CODING":
            return {
                "provider": "advanced-code-model",
                "reason": "Optimized for coding"
            }

        if prompt_quality_score < 50:
            return {
                "provider": "quality-review-pipeline",
                "reason": "Prompt quality too low"
            }

        return {
            "provider": "gemini-1.5-flash",
            "reason": "General workload"
        }

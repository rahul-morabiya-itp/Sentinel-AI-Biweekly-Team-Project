from dataclasses import dataclass
from typing import List


@dataclass
class PromptQualityResult:
    score: int
    issues: List[str]
    recommendations: List[str]


class PromptQualityAnalyzer:

    def analyze(self, prompt: str) -> PromptQualityResult:

        issues = []
        recommendations = []

        score = 100

        word_count = len(prompt.split())

        if word_count > 150:
            score -= 20
            issues.append("Prompt excessively verbose")
            recommendations.append(
                "Reduce unnecessary context and verbosity"
            )

        if "explain everything" in prompt.lower():
            score -= 15
            issues.append("Ambiguous broad instruction")
            recommendations.append(
                "Specify exact output expectations"
            )

        if "please" not in prompt.lower() and len(prompt) < 20:
            score -= 10
            issues.append("Insufficient contextual clarity")
            recommendations.append(
                "Provide additional business context"
            )

        if "json" not in prompt.lower() and "format" not in prompt.lower():
            score -= 10
            recommendations.append(
                "Specify output format for consistency"
            )

        if score >= 85:
            recommendations.append(
                "Prompt structure appears strong"
            )

        score = max(score, 0)

        return PromptQualityResult(
            score=score,
            issues=issues,
            recommendations=recommendations
        )

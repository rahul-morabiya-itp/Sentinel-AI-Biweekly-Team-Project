from dataclasses import dataclass
from typing import List


@dataclass
class RiskAnalysisResult:
    risk_level: str
    detected_categories: List[str]
    recommendations: List[str]


class AdvancedRiskEngine:

    HIGH_RISK_KEYWORDS = {
        "password": "Credential Exposure",
        "secret": "Sensitive Information",
        "salary": "HR Sensitive Data",
        "confidential": "Confidential Business Data",
        "private": "Privacy Risk",
        "token": "Credential Leakage",
        "ssn": "Personal Identity Risk",
        "credit card": "Financial Data Exposure"
    }

    def analyze(self, prompt: str) -> RiskAnalysisResult:

        detected_categories = []

        recommendations = []

        risk_score = 0

        lower_prompt = prompt.lower()

        for keyword, category in self.HIGH_RISK_KEYWORDS.items():

            if keyword in lower_prompt:
                detected_categories.append(category)
                risk_score += 25

        if risk_score >= 50:
            risk_level = "HIGH"
            recommendations.append(
                "Mask sensitive information before sending to external LLM"
            )

        elif risk_score >= 25:
            risk_level = "MEDIUM"
            recommendations.append(
                "Review prompt for sensitive content"
            )

        else:
            risk_level = "LOW"
            recommendations.append(
                "No major risks detected"
            )

        return RiskAnalysisResult(
            risk_level=risk_level,
            detected_categories=detected_categories,
            recommendations=recommendations
        )

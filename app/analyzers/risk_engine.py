RISK_KEYWORDS = [
    "salary",
    "password",
    "secret",
    "confidential",
    "private",
    "api key"
]


def assess_risk(prompt: str):

    lower_prompt = prompt.lower()

    for keyword in RISK_KEYWORDS:

        if keyword in lower_prompt:
            return "HIGH"

    return "LOW"

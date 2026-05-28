class ModelSelector:

    def select_model(
        self,
        intent: str,
        risk_level: str,
        prompt_quality_score: int
    ):

        if risk_level == "HIGH":

            return {
                "provider": "google",
                "model": "gemini-1.5-flash"
            }

        if intent == "SUMMARIZATION":

            return {
                "provider": "google",
                "model": "gemini-1.5-flash-8b"
            }

        if intent == "CODING":

            return {
                "provider": "google",
                "model": "gemini-2.5-flash"
            }

        return {
            "provider": "google",
            "model": "gemini-1.5-flash"
        }


model_selector = ModelSelector()
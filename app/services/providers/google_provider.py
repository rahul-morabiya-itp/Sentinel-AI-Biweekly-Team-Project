import google.generativeai as genai

from google.api_core.exceptions import (
    NotFound
)

from app.core.config import settings


# =========================================================
# GOOGLE PROVIDER
# =========================================================

class GoogleProvider:

    def __init__(self):

        genai.configure(
            api_key=settings.GEMINI_API_KEY
        )

        # =================================================
        # MODEL FALLBACK PRIORITY
        # =================================================

        self.fallback_models = [
            "gemini-3.5-flash",
            "gemini-1.5-flash-8b",
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-pro"
        ]

    # =====================================================
    # MODEL EXECUTION
    # =====================================================

    def generate(
        self,
        model_name: str,
        prompt: str
    ):

        tried_models = []

        models_to_try = [
            model_name
        ] + [
            m for m in self.fallback_models
            if m != model_name
        ]

        last_error = None

        for candidate_model in models_to_try:

            try:

                tried_models.append(
                    candidate_model
                )

                model = genai.GenerativeModel(
                    model_name=candidate_model
                )

                response = model.generate_content(
                    prompt
                )

                response_text = (
                    response.text
                    if hasattr(response, "text")
                    else str(response)
                )

                input_tokens = len(
                    prompt.split()
                )

                output_tokens = len(
                    response_text.split()
                )

                total_tokens = (
                    input_tokens
                    + output_tokens
                )

                return {

                    "provider": "google",

                    "model": candidate_model,

                    "response": response_text,

                    "input_tokens": (
                        input_tokens
                    ),

                    "output_tokens": (
                        output_tokens
                    ),

                    "total_tokens": (
                        total_tokens
                    ),

                    "fallback_used": (
                        candidate_model
                        != model_name
                    ),

                    "tried_models": (
                        tried_models
                    )
                }

            except NotFound as error:

                last_error = error

                continue

            except Exception as error:

                last_error = error

                continue

        raise RuntimeError(
            f"All Gemini models failed. "
            f"Tried models: {tried_models}. "
            f"Last error: {str(last_error)}"
        )
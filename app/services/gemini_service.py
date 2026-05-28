import google.generativeai as genai

from app.core.config import settings


MODEL_NAME = "gemini-1.5-flash-8b"

genai.configure(
    api_key=settings.GEMINI_API_KEY
)

model = genai.GenerativeModel(
    model_name=MODEL_NAME
)


def ask_gemini(prompt: str):

    response = model.generate_content(prompt)

    response_text = response.text

    input_tokens = len(prompt.split())

    output_tokens = len(response_text.split())

    total_tokens = (
        input_tokens + output_tokens
    )

    return {
        "model": MODEL_NAME,
        "response": response_text,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens
    }
def classify_intent(prompt: str):

    text = prompt.lower()

    if "summarize" in text:
        return "SUMMARIZATION"

    if "code" in text:
        return "CODING"

    if "analyze" in text:
        return "ANALYSIS"

    if "translate" in text:
        return "TRANSLATION"

    return "GENERAL"

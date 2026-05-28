def generate_optimizations(prompt: str):

    suggestions = []

    word_count = len(prompt.split())

    if word_count > 120:
        suggestions.append(
            "Prompt is too verbose. Reduce unnecessary context."
        )

    if "explain everything" in prompt.lower():
        suggestions.append(
            "Specify concise output requirements."
        )

    if len(suggestions) == 0:
        suggestions.append(
            "Prompt appears reasonably optimized."
        )

    return suggestions

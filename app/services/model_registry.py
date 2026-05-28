MODEL_REGISTRY = {

    "gemini-1.5-flash-8b": {
        "provider": "google",
        "category": "fast",
        "supports_streaming": True,
        "input_cost_per_million": 0.0375,
        "output_cost_per_million": 0.15
    },

    "gemini-1.5-flash": {
        "provider": "google",
        "category": "balanced",
        "supports_streaming": True,
        "input_cost_per_million": 0.075,
        "output_cost_per_million": 0.30
    },

    # Current Google pricing
    "gemini-2.5-flash": {
        "provider": "google",
        "category": "advanced",
        "supports_streaming": True,
        "input_cost_per_million": 0.30,
        "output_cost_per_million": 2.50
    },

    "gemini-3.5-flash": {
        "provider": "google",
        "category": "advanced",
        "supports_streaming": True,
        "input_cost_per_million": 0.30,
        "output_cost_per_million": 2.50
    },

    "gemini-2.5-pro": {
        "provider": "google",
        "category": "premium",
        "supports_streaming": True,
        "input_cost_per_million": 1.25,
        "output_cost_per_million": 10.00
    },

    # GPT-4o pricing updated
    "openai-gpt4o": {
        "provider": "openai",
        "category": "premium",
        "supports_streaming": True,
        "input_cost_per_million": 2.50,
        "output_cost_per_million": 10.00
    },

    # Claude Sonnet pricing is correct
    "claude-sonnet": {
        "provider": "anthropic",
        "category": "balanced",
        "supports_streaming": True,
        "input_cost_per_million": 3.00,
        "output_cost_per_million": 15.00
    }
}
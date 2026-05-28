from app.services.providers.google_provider import (
    GoogleProvider
)


class ProviderManager:

    def __init__(self):

        self.providers = {
            "google": GoogleProvider()
        }

    def generate(
        self,
        provider_name: str,
        model_name: str,
        prompt: str
    ):

        provider = self.providers.get(
            provider_name
        )

        if not provider:

            raise ValueError(
                f"Provider not found: {provider_name}"
            )

        return provider.generate(
            model_name=model_name,
            prompt=prompt
        )


provider_manager = ProviderManager()
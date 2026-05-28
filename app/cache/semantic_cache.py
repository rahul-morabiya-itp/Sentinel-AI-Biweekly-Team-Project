from typing import Dict


class SemanticCache:

    def __init__(self):

        self.cache = {}

    def get(self, similarity_key: str):

        return self.cache.get(similarity_key)

    def set(
        self,
        similarity_key: str,
        response: Dict
    ):

        self.cache[similarity_key] = response

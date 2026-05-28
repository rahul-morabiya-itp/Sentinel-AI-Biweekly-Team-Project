from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


model = SentenceTransformer("all-MiniLM-L6-v2")

stored_prompts = []

stored_embeddings = []


def check_similarity(prompt: str):

    global stored_prompts
    global stored_embeddings

    embedding = model.encode([prompt])[0]

    if len(stored_embeddings) == 0:

        stored_prompts.append(prompt)

        stored_embeddings.append(embedding)

        return None

    similarities = cosine_similarity(
        [embedding],
        stored_embeddings
    )[0]

    max_score = float(np.max(similarities))

    if max_score > 0.90:

        index = int(np.argmax(similarities))

        return {
            "similar_prompt": stored_prompts[index],
            "score": round(max_score, 4)
        }

    stored_prompts.append(prompt)

    stored_embeddings.append(embedding)

    return None

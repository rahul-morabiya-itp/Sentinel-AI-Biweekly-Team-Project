from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

import numpy as np


# =========================================================
# EMBEDDING MODEL
# =========================================================

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# =========================================================
# IN-MEMORY VECTOR STORE
# =========================================================

stored_prompts = []

stored_embeddings = []

SIMILARITY_THRESHOLD = 0.75

# =========================================================
# SEMANTIC SIMILARITY CHECK
# =========================================================

def check_similarity(prompt: str):

    global stored_prompts
    global stored_embeddings

    # =====================================================
    # EMPTY PROMPT SAFETY
    # =====================================================

    if not prompt.strip():

        return None

    # =====================================================
    # CREATE EMBEDDING
    # =====================================================

    embedding = model.encode(
        [prompt]
    )[0]

    # =====================================================
    # FIRST REQUEST
    # =====================================================

    if len(stored_embeddings) == 0:

        stored_prompts.append(
            prompt
        )

        stored_embeddings.append(
            embedding
        )

        return None

    # =====================================================
    # CALCULATE COSINE SIMILARITY
    # =====================================================

    similarities = cosine_similarity(
        [embedding],
        stored_embeddings
    )[0]

    max_score = float(
        np.max(similarities)
    )

    best_match_index = int(
        np.argmax(similarities)
    )

    # =====================================================
    # MATCH FOUND
    # =====================================================

    if max_score >= SIMILARITY_THRESHOLD:

        similar_prompt = (
            stored_prompts[
                best_match_index
            ]
        )

        # Store current prompt too
        stored_prompts.append(
            prompt
        )

        stored_embeddings.append(
            embedding
        )

        return {

            "similar_prompt": (
                similar_prompt
            ),

            "score": round(
                max_score,
                4
            )
        }

    # =====================================================
    # STORE NEW PROMPT
    # =====================================================

    stored_prompts.append(
        prompt
    )

    stored_embeddings.append(
        embedding
    )

    return None

# =========================================================
# DEBUG / METRICS
# =========================================================

def get_similarity_stats():

    return {

        "stored_prompts": len(
            stored_prompts
        ),

        "stored_embeddings": len(
            stored_embeddings
        ),

        "similarity_threshold": (
            SIMILARITY_THRESHOLD
        )
    }
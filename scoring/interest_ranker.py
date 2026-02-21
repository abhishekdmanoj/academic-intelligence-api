import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from embeddings.model import load_embedding_model

def rank_units_by_interest(embeddings, metadata, interest_text, top_k=5):
    model = load_embedding_model()

    # Embed interest
    interest_embedding = model.encode([interest_text])

    # Compute cosine similarity
    similarities = cosine_similarity(interest_embedding, embeddings)[0]

    # Combine scores with metadata
    ranked = []
    for i, score in enumerate(similarities):
        ranked.append({
            "subject": metadata[i]["subject"],
            "unit": metadata[i]["unit"],
            "score": float(score)
        })

    # Sort by score (descending)
    ranked.sort(key=lambda x: x["score"], reverse=True)

    return ranked[:top_k]

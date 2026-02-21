from sklearn.metrics.pairwise import cosine_similarity
from embeddings.model import load_embedding_model


def rank_universities(university_data, interest_text, top_units=5):
    model = load_embedding_model()
    interest_embedding = model.encode([interest_text])

    results = []

    for uni in university_data:
        if len(uni["embeddings"]) == 0:
            continue

        similarities = cosine_similarity(
            interest_embedding, uni["embeddings"]
        )[0]

        unit_scores = []

        for i, score in enumerate(similarities):
            unit_scores.append({
                "unit": uni["metadata"][i]["unit"],
                "raw_score": float(score)
            })

        unit_scores.sort(key=lambda x: x["raw_score"], reverse=True)

        top_unit_scores = unit_scores[:top_units]

        if not top_unit_scores:
            continue

        max_unit_score = top_unit_scores[0]["raw_score"]

        formatted_units = []

        for u in top_unit_scores:
            percent = (
                (u["raw_score"] / max_unit_score) * 100
                if max_unit_score > 0 else 0
            )

            formatted_units.append({
                "unit": u["unit"],
                "relevance_percent": round(percent, 2)
            })

        syllabus_score = sum(u["raw_score"] for u in top_unit_scores) / len(top_unit_scores)

        results.append({
            "university": uni["university"],
            "raw_score": syllabus_score,
            "top_units": formatted_units
        })

    if not results:
        return {"rankings": []}

    # Sort universities
    results.sort(key=lambda x: x["raw_score"], reverse=True)

    max_uni_score = results[0]["raw_score"]

    final_rankings = []

    for uni in results:
        percent = (
            (uni["raw_score"] / max_uni_score) * 100
            if max_uni_score > 0 else 0
        )

        final_rankings.append({
            "university": uni["university"],
            "relevance_percent": round(percent, 2),
            "top_units": uni["top_units"]
        })

    return {"rankings": final_rankings}
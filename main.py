import os
from utils.document_loader import extract_text
from utils.text_chunker import chunk_by_units
from embeddings.embed_chunks import embed_chunks
from scoring.syllabus_ranker import rank_universities
from utils.pyq_loader import load_pyqs
from embeddings.embed_pyqs import embed_pyqs
from vector_store.pyq_index import PyqIndex
from scoring.pyq_retriever import retrieve_pyqs
from ingestion.registry_manager import get_active_documents


# 🔥 Determine project root (important for Render)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def run_university_ranking(interest_text):
    university_data = []

    active_docs = get_active_documents()

    for doc in active_docs:
        # ✅ FIXED PATH RESOLUTION
        file_path = os.path.join(PROJECT_ROOT, doc["file_path"])
        university_name = doc["university"]

        text = extract_text(file_path)
        print(f"\n📄 {university_name} — Extracted text length:", len(text))

        chunks = chunk_by_units(text)
        print("🔹 Chunks found:", len(chunks))

        if not chunks:
            print(f"⚠ No chunks detected for {university_name}. Skipping.")
            continue

        embeddings, metadata = embed_chunks(chunks)

        if embeddings is None or len(embeddings) == 0:
            print(f"⚠ No embeddings generated for {university_name}. Skipping.")
            continue

        university_data.append({
            "university": university_name,
            "embeddings": embeddings,
            "metadata": metadata
        })

    if not university_data:
        print("❌ No valid university data available for ranking.")
        return []

    return rank_universities(university_data, interest_text)


def run_pyq_retrieval(entrance, subject, interest_text):
    # ✅ FIXED PYQ PATH
    pyq_path = os.path.join(PROJECT_ROOT, "data", "pyqs", entrance, f"{subject}.txt")

    pyqs = load_pyqs(pyq_path)
    pyq_embeddings = embed_pyqs(pyqs)

    index = PyqIndex(pyq_embeddings.shape[1])
    index.add(pyq_embeddings)

    return retrieve_pyqs(
        interest_text=interest_text,
        pyqs=pyqs,
        pyq_index=index,
        top_k=3
    )


if __name__ == "__main__":
    interest = "calculus, limits and functions"

    print("\n=== Ranked Universities ===")
    uni_results = run_university_ranking(interest)

    for r in uni_results:
        print(f"\n{r['university']} → Score: {round(r['score'], 3)}")
        for u in r["top_units"]:
            print("  -", u["unit"], "→", round(u["score"], 3))

    print("\n=== Related PYQs (JEE - Mathematics) ===")
    pyq_results = run_pyq_retrieval(
        entrance="jee",
        subject="mathematics",
        interest_text=interest
    )

    for q in pyq_results:
        print("-", q)
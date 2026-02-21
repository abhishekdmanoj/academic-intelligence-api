from embeddings.model import load_embedding_model

def retrieve_pyqs(interest_text, pyqs, pyq_index, top_k=3):
    model = load_embedding_model()
    query_embedding = model.encode([interest_text])
    indices = pyq_index.search(query_embedding, top_k=top_k)[0]
    return [pyqs[i] for i in indices]

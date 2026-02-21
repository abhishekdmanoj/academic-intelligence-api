import numpy as np
from embeddings.model import load_embedding_model

def embed_chunks(chunks):
    model = load_embedding_model()

    texts = []
    metadata = []

    for chunk in chunks:
        combined_text = f"{chunk['subject']} {chunk['unit']} {chunk['text']}"
        texts.append(combined_text)
        metadata.append({
            "subject": chunk["subject"],
            "unit": chunk["unit"]
        })

    embeddings = model.encode(texts, show_progress_bar=True)

    return np.array(embeddings), metadata

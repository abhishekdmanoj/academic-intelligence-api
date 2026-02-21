import numpy as np
from embeddings.model import load_embedding_model

def embed_pyqs(pyqs):
    
    if not pyqs:
        raise ValueError("No PYQs loaded. Check PYQ file path or content.")
    
    model = load_embedding_model()
    embeddings = model.encode(pyqs, show_progress_bar=True)
    return np.array(embeddings)

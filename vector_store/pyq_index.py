import faiss

class PyqIndex:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)

    def add(self, embeddings):
        self.index.add(embeddings)

    def search(self, query_embedding, top_k=3):
        _, indices = self.index.search(query_embedding, top_k)
        return indices

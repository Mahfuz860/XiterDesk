from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

def chunk_text(text, size=300):
    words = text.split()
    chunks = []

    for i in range(0, len(words), size):
        chunk = " ".join(words[i:i+size])
        chunks.append(chunk)

    return chunks

class PDFIndexer:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = None
        self.chunks = []

    def build(self, pages):
        all_chunks = []
        for p in pages:
            chunks = chunk_text(p["text"])
            for c in chunks:
                all_chunks.append({
                    "page": p["page"],
                    "text": c
                })

        self.chunks = all_chunks

        texts = [c["text"] for c in all_chunks]
        embeddings = self.model.encode(texts, convert_to_numpy=True)

        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

    def search(self, query, top_k=3):
        query_vec = self.model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vec, top_k)

        results = []
        for idx in indices[0]:
            results.append(self.chunks[idx])

        return results

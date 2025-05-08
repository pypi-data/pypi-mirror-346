import faiss
import numpy as np
import uuid


class FAISSHelper:
    def __init__(self, dim=384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata_store = {}  # id -> {"text": ..., "meta": ...}

    def insert(self, vectors: list, documents: list, metadatas: list = None, ids: list = None):
        if not ids:
            ids = [str(uuid.uuid4()) for _ in documents]
        if not metadatas:
            metadatas = [{} for _ in documents]

        try:
            self.index.add(np.array(vectors).astype("float32"))
            for i, doc, meta in zip(ids, documents, metadatas):
                self.metadata_store[i] = {"text": doc, "metadata": meta}
            return ids
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to insert into FAISS: {e}")

    def query(self, embedding_vector: list, top_k: int = 5):
        try:
            D, I = self.index.search(np.array([embedding_vector]).astype("float32"), top_k)
            result_ids = list(self.metadata_store.keys())
            results = []
            for idx in I[0]:
                if idx < len(result_ids):
                    _id = result_ids[idx]
                    results.append({
                        "id": _id,
                        "text": self.metadata_store[_id]["text"],
                        "metadata": self.metadata_store[_id]["metadata"]
                    })
            return results
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to query FAISS: {e}")

    def count(self):
        return self.index.ntotal

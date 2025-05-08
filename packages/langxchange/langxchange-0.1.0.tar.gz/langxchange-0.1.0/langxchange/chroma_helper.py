import os
import uuid
import chromadb
from chromadb.config import Settings


class ChromaHelper:
    def __init__(self, collection_name: str = "langxchange_collection", persist_path: str = None):
        persist_path = persist_path or os.getenv("CHROMA_PERSIST_PATH", "./chroma_storage")

        self.client = chromadb.Client(
            Settings(chroma_db_impl="duckdb+parquet", persist_directory=persist_path)
        )
        self.collection = self.client.get_or_create_collection(name=collection_name)

    def insert(self, documents: list, embeddings: list, metadatas: list = None, ids: list = None):
        if not ids:
            ids = [str(uuid.uuid4()) for _ in documents]
        if not metadatas:
            metadatas = [{} for _ in documents]

        try:
            self.collection.add(
                ids=ids,
                documents=documents,
                embeddings=embeddings,
                metadatas=metadatas
            )
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to insert into Chroma: {e}")

        return ids

    def query(self, embedding_vector: list, top_k: int = 5, include_metadata: bool = True):
        try:
            results = self.collection.query(
                query_embeddings=[embedding_vector],
                n_results=top_k,
                include=["documents", "metadatas"] if include_metadata else ["documents"]
            )
            return results
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Failed to query Chroma: {e}")

    def get_collection_count(self):
        try:
            return len(self.collection.get()["ids"])
        except Exception as e:
            raise RuntimeError(f"[❌ ERROR] Could not get Chroma collection count: {e}")

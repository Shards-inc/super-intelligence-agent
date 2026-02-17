from typing import List, Dict, Any, Optional
import os
from qdrant_client import QdrantClient
from qdrant_client.http import models
from sentence_transformers import SentenceTransformer

class VectorMemory:
    def __init__(self, collection_name: str = "agent_memory"):
        self.client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))
        self.collection_name = collection_name
        self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
        self._setup_collection()

    def _setup_collection(self):
        collections = self.client.get_collections().collections
        exists = any(c.name == self.collection_name for c in collections)
        if not exists:
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=models.VectorParams(size=384, distance=models.Distance.COSINE),
            )

    def add_memory(self, text: str, metadata: Dict[str, Any] = {}):
        vector = self.encoder.encode(text).tolist()
        self.client.upsert(
            collection_name=self.collection_name,
            points=[
                models.PointStruct(
                    id=hash(text) % (10**10), # Simple hash for ID
                    vector=vector,
                    payload={"text": text, **metadata}
                )
            ]
        )

    def search_memory(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        vector = self.encoder.encode(query).tolist()
        results = self.client.search(
            collection_name=self.collection_name,
            query_vector=vector,
            limit=limit
        )
        return [hit.payload for hit in results]

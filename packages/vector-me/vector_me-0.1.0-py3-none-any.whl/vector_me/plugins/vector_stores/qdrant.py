from typing import List, Dict, Any, Optional
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from vector_me.plugins.base import BaseVectorStore, VectorStoreConfig

class QdrantVectorStore(BaseVectorStore):
    """Qdrant vector store implementation."""

    def __init__(self):
        """Initialize Qdrant vector store."""
        self._client = None
        self._collection_name = None

    def _get_client(self, config: VectorStoreConfig) -> QdrantClient:
        """Get or create Qdrant client."""
        if config.host and config.port:
            return QdrantClient(host=config.host, port=config.port)
        return QdrantClient(path=config.persist_directory)

    def _ensure_collection(self, config: VectorStoreConfig, vector_size: int) -> None:
        """Ensure collection exists."""
        self._client = self._get_client(config)
        self._collection_name = config.collection_name

        # Create collection if it doesn't exist
        self._client.create_collection(
            collection_name=self._collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE)
        )

    def add_texts(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: List[Dict[str, Any]],
        config: Optional[VectorStoreConfig] = None
    ) -> None:
        """Add texts and their embeddings to Qdrant."""
        if not config:
            raise ValueError("VectorStoreConfig is required")

        # Ensure collection exists
        self._ensure_collection(config, len(embeddings[0]))

        # Prepare points
        points = []
        for i, (text, embedding, metadata) in enumerate(zip(texts, embeddings, metadatas)):
            points.append(
                PointStruct(
                    id=i,
                    vector=embedding,
                    payload={"text": text, "metadata": metadata}
                )
            )

        # Add points to collection
        self._client.upsert(
            collection_name=self._collection_name,
            points=points
        )

    def search(
        self,
        query: str,
        query_embedding: List[float],
        k: int = 4,
        config: Optional[VectorStoreConfig] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar texts in Qdrant."""
        if not config:
            raise ValueError("VectorStoreConfig is required")

        # Ensure client and collection are set
        self._client = self._get_client(config)
        self._collection_name = config.collection_name

        # Search for similar vectors
        results = self._client.search(
            collection_name=self._collection_name,
            query_vector=query_embedding,
            limit=k
        )

        # Format results
        return [
            {
                "text": point.payload["text"],
                "metadata": point.payload["metadata"],
                "distance": point.score
            }
            for point in results.points
        ]

    def save(self, config: VectorStoreConfig) -> None:
        """Save is not needed for Qdrant as it persists automatically."""
        pass 
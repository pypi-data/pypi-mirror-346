from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from ..base import BaseVectorStore, VectorStoreConfig

class ChromaVectorStore(BaseVectorStore):
    """Chroma vector store implementation."""
    
    def __init__(self):
        self._client = None
        self._collection = None
    
    def _get_client(self, config: VectorStoreConfig):
        if self._client is None:
            self._client = chromadb.PersistentClient(
                path=config.persist_directory,
                settings=Settings(
                    anonymized_telemetry=False
                )
            )
        return self._client
    
    def _get_collection(self, config: VectorStoreConfig):
        if self._collection is None:
            client = self._get_client(config)
            try:
                self._collection = client.get_collection(config.collection_name)
            except ValueError:
                self._collection = client.create_collection(config.collection_name)
        return self._collection
    
    def add_texts(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        config: Optional[VectorStoreConfig] = None
    ) -> None:
        """Add texts and their embeddings to Chroma."""
        if not config:
            raise ValueError("VectorStoreConfig is required")
        
        collection = self._get_collection(config)
        collection.add(
            embeddings=embeddings,
            documents=texts,
            metadatas=metadatas or [{}] * len(texts),
            ids=[str(i) for i in range(len(texts))]
        )
    
    def search(
        self,
        query: str,
        query_embedding: List[float],
        k: int = 4,
        config: Optional[VectorStoreConfig] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar texts in Chroma."""
        if not config:
            raise ValueError("VectorStoreConfig is required")
        
        collection = self._get_collection(config)
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=k
        )
        
        return [
            {
                "text": doc,
                "metadata": meta,
                "distance": dist
            }
            for doc, meta, dist in zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0]
            )
        ]
    
    def save(self, config: Optional[VectorStoreConfig] = None) -> None:
        """Save is not needed for Chroma as it persists automatically."""
        pass 
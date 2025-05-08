from typing import List, Dict, Any, Optional
import numpy as np
import faiss
import pickle
from pathlib import Path
from ..base import BaseVectorStore, VectorStoreConfig

class FAISSVectorStore(BaseVectorStore):
    """FAISS vector store implementation."""
    
    def __init__(self):
        self._index = None
        self._texts = []
        self._metadatas = []
    
    def _create_index(self, dim: int):
        """Create a new FAISS index."""
        self._index = faiss.IndexFlatL2(dim)
    
    def add_texts(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        config: Optional[VectorStoreConfig] = None
    ) -> None:
        """Add texts and their embeddings to FAISS."""
        if not config:
            raise ValueError("VectorStoreConfig is required")
        
        # Convert embeddings to numpy array
        embeddings_array = np.array(embeddings).astype('float32')
        
        # Create index if it doesn't exist
        if self._index is None:
            self._create_index(embeddings_array.shape[1])
        
        # Add vectors to index
        self._index.add(embeddings_array)
        
        # Store texts and metadatas
        self._texts.extend(texts)
        self._metadatas.extend(metadatas or [{}] * len(texts))
    
    def search(
        self,
        query: str,
        query_embedding: List[float],
        k: int = 4,
        config: Optional[VectorStoreConfig] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar texts in FAISS."""
        if not config:
            raise ValueError("VectorStoreConfig is required")
        
        if self._index is None:
            return []
        
        # Convert query embedding to numpy array
        query_array = np.array([query_embedding]).astype('float32')
        
        # Search in index
        distances, indices = self._index.search(query_array, k)
        
        # Return results
        return [
            {
                "text": self._texts[idx],
                "metadata": self._metadatas[idx],
                "distance": float(dist)
            }
            for idx, dist in zip(indices[0], distances[0])
            if idx != -1  # FAISS returns -1 for empty slots
        ]
    
    def save(self, config: Optional[VectorStoreConfig] = None) -> None:
        """Save the FAISS index and associated data to disk."""
        if not config or not config.persist_directory:
            raise ValueError("VectorStoreConfig with persist_directory is required")
        
        persist_dir = Path(config.persist_directory)
        persist_dir.mkdir(parents=True, exist_ok=True)
        
        # Save index
        faiss.write_index(self._index, str(persist_dir / "index.faiss"))
        
        # Save texts and metadatas
        with open(persist_dir / "data.pkl", "wb") as f:
            pickle.dump({
                "texts": self._texts,
                "metadatas": self._metadatas
            }, f)
    
    def load(self, config: Optional[VectorStoreConfig] = None) -> None:
        """Load the FAISS index and associated data from disk."""
        if not config or not config.persist_directory:
            raise ValueError("VectorStoreConfig with persist_directory is required")
        
        persist_dir = Path(config.persist_directory)
        
        # Load index
        self._index = faiss.read_index(str(persist_dir / "index.faiss"))
        
        # Load texts and metadatas
        with open(persist_dir / "data.pkl", "rb") as f:
            data = pickle.load(f)
            self._texts = data["texts"]
            self._metadatas = data["metadatas"] 
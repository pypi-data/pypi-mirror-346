from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from pydantic import BaseModel

class ChunkerConfig(BaseModel):
    """Base configuration for chunkers."""
    chunk_size: int = 1000
    chunk_overlap: int = 200
    separator: str = "\n\n"

class EmbedderConfig(BaseModel):
    """Base configuration for embedders."""
    model_name: str
    api_key: Optional[str] = None
    device: str = "cpu"

class VectorStoreConfig(BaseModel):
    """Base configuration for vector stores."""
    collection_name: str
    persist_directory: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None

class BaseChunker(ABC):
    """Base class for text chunkers."""
    
    @abstractmethod
    def chunk(self, text: str, config: ChunkerConfig) -> List[str]:
        """Split text into chunks."""
        pass

class BaseEmbedder(ABC):
    """Base class for text embedders."""
    
    @abstractmethod
    def embed(self, texts: List[str], config: EmbedderConfig) -> List[List[float]]:
        """Generate embeddings for texts."""
        pass

class BaseVectorStore(ABC):
    """Base class for vector stores."""
    
    @abstractmethod
    def add_texts(
        self,
        texts: List[str],
        embeddings: List[List[float]],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        config: Optional[VectorStoreConfig] = None
    ) -> None:
        """Add texts and their embeddings to the vector store."""
        pass
    
    @abstractmethod
    def search(
        self,
        query: str,
        query_embedding: List[float],
        k: int = 4,
        config: Optional[VectorStoreConfig] = None
    ) -> List[Dict[str, Any]]:
        """Search for similar texts in the vector store."""
        pass
    
    @abstractmethod
    def save(self, config: Optional[VectorStoreConfig] = None) -> None:
        """Save the vector store to disk."""
        pass 
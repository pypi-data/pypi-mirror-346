from typing import List
from sentence_transformers import SentenceTransformer
from ..base import BaseEmbedder, EmbedderConfig

class HuggingFaceEmbedder(BaseEmbedder):
    """HuggingFace embeddings implementation."""
    
    def __init__(self):
        self._model = None
    
    def embed(self, texts: List[str], config: EmbedderConfig) -> List[List[float]]:
        """Generate embeddings using HuggingFace models."""
        if self._model is None or self._model.get_config_dict()["model_name"] != config.model_name:
            self._model = SentenceTransformer(config.model_name, device=config.device)
        
        return self._model.encode(texts, convert_to_list=True) 
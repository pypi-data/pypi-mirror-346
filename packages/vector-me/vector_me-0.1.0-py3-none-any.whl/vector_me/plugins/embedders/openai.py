from typing import List
import openai
from ..base import BaseEmbedder, EmbedderConfig

class OpenAIEmbedder(BaseEmbedder):
    """OpenAI embeddings implementation."""
    
    def embed(self, texts: List[str], config: EmbedderConfig) -> List[List[float]]:
        """Generate embeddings using OpenAI's API."""
        if not config.api_key:
            raise ValueError("OpenAI API key is required")
        
        openai.api_key = config.api_key
        response = openai.embeddings.create(
            model=config.model_name,
            input=texts
        )
        return [data.embedding for data in response.data] 
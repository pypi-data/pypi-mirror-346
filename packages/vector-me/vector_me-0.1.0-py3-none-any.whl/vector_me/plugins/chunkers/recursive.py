from typing import List
from langchain.text_splitter import RecursiveCharacterTextSplitter
from ..base import BaseChunker, ChunkerConfig

class RecursiveChunker(BaseChunker):
    """Recursive character text splitter implementation."""
    
    def chunk(self, text: str, config: ChunkerConfig) -> List[str]:
        """Split text into chunks using recursive character splitting."""
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            separators=[config.separator, "\n", " ", ""]
        )
        return splitter.split_text(text) 
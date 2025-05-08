import pytest
import numpy as np
from pathlib import Path
from vector_me.plugins.base import ChunkerConfig, EmbedderConfig, VectorStoreConfig

@pytest.fixture
def temp_dir(tmp_path):
    """Create a temporary directory for testing."""
    return tmp_path

@pytest.fixture
def sample_texts():
    """Sample texts for testing."""
    return [
        "This is the first test document.",
        "This is the second test document.",
        "This is the third test document.",
    ]

@pytest.fixture
def sample_embeddings():
    """Sample embeddings for testing."""
    return [
        [0.1, 0.2, 0.3],
        [0.4, 0.5, 0.6],
        [0.7, 0.8, 0.9],
    ]

@pytest.fixture
def sample_metadatas():
    """Sample metadata for testing."""
    return [
        {"source": "test1.txt", "page": 1},
        {"source": "test2.txt", "page": 2},
        {"source": "test3.txt", "page": 3},
    ]

@pytest.fixture
def chunker_config():
    """Default chunker configuration."""
    return ChunkerConfig(
        chunk_size=100,
        chunk_overlap=20,
        separator="\n"
    )

@pytest.fixture
def embedder_config():
    """Default embedder configuration."""
    return EmbedderConfig(
        model_name="test-model",
        api_key="test-key",
        device="cpu"
    )

@pytest.fixture
def vector_store_config(temp_dir):
    """Default vector store configuration."""
    return VectorStoreConfig(
        collection_name="test-collection",
        persist_directory=str(temp_dir)
    ) 
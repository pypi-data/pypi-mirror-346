import pytest
import numpy as np
from vector_me.plugins.vector_stores.faiss import FAISSVectorStore

def test_faiss_initialization():
    """Test FAISS vector store initialization."""
    store = FAISSVectorStore()
    assert store._index is None
    assert store._texts == []
    assert store._metadatas == []

def test_faiss_add_texts(sample_texts, sample_embeddings, sample_metadatas, vector_store_config):
    """Test adding texts to FAISS vector store."""
    store = FAISSVectorStore()
    
    # Add texts
    store.add_texts(
        texts=sample_texts,
        embeddings=sample_embeddings,
        metadatas=sample_metadatas,
        config=vector_store_config
    )
    
    # Check if texts and metadatas were stored
    assert len(store._texts) == len(sample_texts)
    assert len(store._metadatas) == len(sample_metadatas)
    assert store._texts == sample_texts
    assert store._metadatas == sample_metadatas
    
    # Check if index was created
    assert store._index is not None
    assert store._index.ntotal == len(sample_texts)

def test_faiss_search(sample_texts, sample_embeddings, sample_metadatas, vector_store_config):
    """Test searching in FAISS vector store."""
    store = FAISSVectorStore()
    
    # Add texts
    store.add_texts(
        texts=sample_texts,
        embeddings=sample_embeddings,
        metadatas=sample_metadatas,
        config=vector_store_config
    )
    
    # Search with first embedding
    results = store.search(
        query="test query",
        query_embedding=sample_embeddings[0],
        k=2,
        config=vector_store_config
    )
    
    # Check results
    assert len(results) == 2
    assert results[0]["text"] == sample_texts[0]  # Should be most similar
    assert results[0]["metadata"] == sample_metadatas[0]
    assert "distance" in results[0]

def test_faiss_save_load(sample_texts, sample_embeddings, sample_metadatas, vector_store_config):
    """Test saving and loading FAISS vector store."""
    store = FAISSVectorStore()
    
    # Add texts
    store.add_texts(
        texts=sample_texts,
        embeddings=sample_embeddings,
        metadatas=sample_metadatas,
        config=vector_store_config
    )
    
    # Save store
    store.save(vector_store_config)
    
    # Create new store and load
    new_store = FAISSVectorStore()
    new_store.load(vector_store_config)
    
    # Check if data was loaded correctly
    assert new_store._texts == store._texts
    assert new_store._metadatas == store._metadatas
    assert new_store._index.ntotal == store._index.ntotal

def test_faiss_invalid_config():
    """Test FAISS vector store with invalid configuration."""
    store = FAISSVectorStore()
    
    with pytest.raises(ValueError):
        store.add_texts(
            texts=["test"],
            embeddings=[[0.1, 0.2, 0.3]],
            config=None
        )
    
    with pytest.raises(ValueError):
        store.search(
            query="test",
            query_embedding=[0.1, 0.2, 0.3],
            config=None
        )
    
    with pytest.raises(ValueError):
        store.save(None)
    
    with pytest.raises(ValueError):
        store.load(None) 
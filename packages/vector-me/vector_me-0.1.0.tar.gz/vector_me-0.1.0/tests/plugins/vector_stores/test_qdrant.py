import pytest
from unittest.mock import patch, MagicMock
from vector_me.plugins.vector_stores.qdrant import QdrantVectorStore
from vector_me.plugins.base import VectorStoreConfig

@pytest.fixture
def vector_store_config():
    return VectorStoreConfig(
        collection_name="test-collection",
        persist_directory="/tmp/test-qdrant"
    )

@pytest.fixture
def mock_qdrant_client():
    with patch("vector_me.plugins.vector_stores.qdrant.QdrantClient") as mock:
        yield mock

def test_qdrant_initialization():
    """Test Qdrant vector store initialization."""
    store = QdrantVectorStore()
    assert store._client is None
    assert store._collection_name is None

def test_qdrant_get_client_local(vector_store_config, mock_qdrant_client):
    """Test getting local Qdrant client."""
    store = QdrantVectorStore()
    with patch("vector_me.plugins.vector_stores.qdrant.QdrantClient", mock_qdrant_client):
        client = store._get_client(vector_store_config)
        assert client == mock_qdrant_client.return_value
        mock_qdrant_client.assert_called_once_with(path=vector_store_config.persist_directory)

def test_qdrant_get_client_remote(vector_store_config, mock_qdrant_client):
    """Test getting remote Qdrant client."""
    vector_store_config.host = "localhost"
    vector_store_config.port = 6333

    store = QdrantVectorStore()
    with patch("vector_me.plugins.vector_stores.qdrant.QdrantClient", mock_qdrant_client):
        client = store._get_client(vector_store_config)
        assert client == mock_qdrant_client.return_value
        mock_qdrant_client.assert_called_once_with(host="localhost", port=6333)

def test_qdrant_ensure_collection(vector_store_config, mock_qdrant_client):
    """Test ensuring collection exists."""
    store = QdrantVectorStore()
    with patch("vector_me.plugins.vector_stores.qdrant.QdrantClient", mock_qdrant_client):
        store._ensure_collection(vector_store_config, vector_size=1536)
        mock_qdrant_client.return_value.create_collection.assert_called_once_with(
            collection_name=vector_store_config.collection_name,
            vectors_config={"size": 1536, "distance": "Cosine"}
        )

def test_qdrant_add_texts(vector_store_config, mock_qdrant_client):
    """Test adding texts to Qdrant."""
    store = QdrantVectorStore()
    texts = ["test1", "test2"]
    embeddings = [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]]
    metadatas = [{"source": "test1.txt"}, {"source": "test2.txt"}]

    with patch("vector_me.plugins.vector_stores.qdrant.QdrantClient", mock_qdrant_client):
        store.add_texts(texts, embeddings, metadatas, vector_store_config)
        mock_qdrant_client.return_value.upsert.assert_called_once()

def test_qdrant_search(vector_store_config, mock_qdrant_client):
    """Test searching in Qdrant."""
    store = QdrantVectorStore()
    query = "test query"
    query_embedding = [0.1, 0.2, 0.3]
    mock_result = MagicMock()
    mock_result.points = [
        MagicMock(
            payload={"text": "test1", "metadata": {"source": "test1.txt"}},
            score=0.9
        )
    ]
    mock_qdrant_client.return_value.search.return_value = mock_result

    with patch("vector_me.plugins.vector_stores.qdrant.QdrantClient", mock_qdrant_client):
        results = store.search(query, query_embedding, config=vector_store_config)
        assert len(results) == 1
        assert results[0]["text"] == "test1"
        assert results[0]["metadata"] == {"source": "test1.txt"}
        assert results[0]["distance"] == 0.9

def test_qdrant_invalid_config():
    """Test handling invalid configuration."""
    store = QdrantVectorStore()
    with pytest.raises(ValueError):
        store.add_texts(["test"], [[0.1, 0.2, 0.3]], [{"source": "test.txt"}], None) 
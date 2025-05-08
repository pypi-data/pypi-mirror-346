import pytest
from pathlib import Path
from typer.testing import CliRunner
from vector_me.cli import app
from unittest.mock import patch, MagicMock

@pytest.fixture
def runner():
    """Create a CLI runner."""
    return CliRunner()

@pytest.fixture
def temp_input_dir(tmp_path):
    """Create a temporary input directory with test files."""
    input_dir = tmp_path / "input"
    input_dir.mkdir()
    
    # Create test files
    (input_dir / "test1.txt").write_text("This is test file 1.")
    (input_dir / "test2.txt").write_text("This is test file 2.")
    
    return input_dir

@pytest.fixture
def temp_output_dir(tmp_path):
    """Create a temporary output directory."""
    output_dir = tmp_path / "output"
    output_dir.mkdir()
    return output_dir

def test_build_command_help(runner):
    """Test build command help message."""
    result = runner.invoke(app, ["build", "--help"])
    assert result.exit_code == 0
    assert "Build a vector database from files in a directory" in result.output

def test_build_command_missing_args(runner):
    """Test build command with missing arguments."""
    result = runner.invoke(app, ["build"])
    assert result.exit_code != 0
    assert "Missing argument" in result.output

def test_build_command_invalid_dirs(runner, tmp_path):
    """Test build command with invalid directories."""
    nonexistent = tmp_path / "nonexistent"
    output = tmp_path / "output"
    output.mkdir()
    result = runner.invoke(app, ["build", str(nonexistent), str(output)])
    assert result.exit_code != 0
    assert "does not exist" in result.output

def test_build_command_invalid_vector_store(runner, temp_input_dir, temp_output_dir):
    """Test build command with invalid vector store."""
    # Create a test file
    test_file = temp_input_dir / "test.txt"
    test_file.write_text("This is a test file.")

    result = runner.invoke(app, [
        "build",
        str(temp_input_dir),
        str(temp_output_dir),
        "--vector-store", "invalid"
    ])
    assert result.exit_code != 0
    assert "Unsupported vector store" in result.output

def test_build_command_openai_missing_key(runner, temp_input_dir, temp_output_dir):
    """Test build command with OpenAI embedder but missing API key."""
    # Create a test file
    test_file = temp_input_dir / "test.txt"
    test_file.write_text("This is a test file.")

    with patch.dict("os.environ", {}, clear=True):
        result = runner.invoke(app, [
            "build",
            str(temp_input_dir),
            str(temp_output_dir),
            "--embedding-provider", "openai"
        ])
        assert result.exit_code != 0
        assert "OpenAI API key is required" in result.output

def test_build_command_success(runner, temp_input_dir, temp_output_dir, monkeypatch):
    """Test successful build command execution."""
    # Create a test file
    test_file = temp_input_dir / "test.txt"
    test_file.write_text("This is a test file.")

    # Mock OpenAI API
    def mock_embeddings_create(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.data = [type("obj", (object,), {"embedding": [0.1, 0.2, 0.3]})()]
        return MockResponse()

    # Mock ChromaDB
    mock_chroma = MagicMock()
    mock_chroma_client = MagicMock()
    mock_chroma.return_value = mock_chroma_client

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("openai.resources.embeddings.Embeddings.create", mock_embeddings_create)
    monkeypatch.setattr("chromadb.Client", mock_chroma)

    result = runner.invoke(app, [
        "build",
        str(temp_input_dir),
        str(temp_output_dir),
        "--embedding-provider", "openai",
        "--vector-store", "chroma"
    ])
    assert result.exit_code == 0
    assert "Vector database built successfully" in result.output

def test_build_command_with_options(runner, temp_input_dir, temp_output_dir, monkeypatch):
    """Test build command with all options."""
    # Create a test file
    test_file = temp_input_dir / "test.txt"
    test_file.write_text("This is a test file.")

    # Mock OpenAI API
    def mock_embeddings_create(*args, **kwargs):
        class MockResponse:
            def __init__(self):
                self.data = [type("obj", (object,), {"embedding": [0.1, 0.2, 0.3]})()]
        return MockResponse()

    # Mock ChromaDB
    mock_chroma = MagicMock()
    mock_chroma_client = MagicMock()
    mock_chroma.return_value = mock_chroma_client

    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setattr("openai.resources.embeddings.Embeddings.create", mock_embeddings_create)
    monkeypatch.setattr("chromadb.Client", mock_chroma)

    result = runner.invoke(app, [
        "build",
        str(temp_input_dir),
        str(temp_output_dir),
        "--embedding-provider", "openai",
        "--embedding-model", "text-embedding-3-small",
        "--vector-store", "chroma",
        "--chunk-size", "1000",
        "--chunk-overlap", "200"
    ])
    assert result.exit_code == 0
    assert "Vector database built successfully" in result.output 
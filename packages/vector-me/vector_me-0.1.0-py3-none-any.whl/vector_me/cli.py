import os
import typer
from pathlib import Path
from typing import Optional
from rich import print

from vector_me.plugins.chunkers.recursive import RecursiveChunker
from vector_me.plugins.embedders.openai import OpenAIEmbedder
from vector_me.plugins.embedders.huggingface import HuggingFaceEmbedder
from vector_me.plugins.vector_stores.chroma import ChromaVectorStore
from vector_me.plugins.vector_stores.faiss import FAISSVectorStore
from vector_me.plugins.vector_stores.qdrant import QdrantVectorStore
from vector_me.plugins.base import ChunkerConfig, EmbedderConfig, VectorStoreConfig

app = typer.Typer()

@app.command()
def build(
    input_dir: str = typer.Argument(..., help="Directory containing files to process"),
    output_dir: str = typer.Argument(..., help="Directory to store the vector database"),
    chunk_size: int = typer.Option(1000, help="Size of text chunks"),
    chunk_overlap: int = typer.Option(200, help="Overlap between chunks"),
    embedding_provider: str = typer.Option("openai", help="Embedding provider (openai or huggingface)"),
    embedding_model: str = typer.Option("text-embedding-3-small", help="Embedding model to use"),
    vector_store: str = typer.Option("chroma", help="Vector store type (chroma, faiss, or qdrant)"),
    qdrant_host: Optional[str] = typer.Option(None, help="Qdrant server host"),
    qdrant_port: Optional[int] = typer.Option(None, help="Qdrant server port"),
):
    """Build a vector database from files in a directory."""
    try:
        # Convert string paths to Path objects
        input_path = Path(input_dir)
        output_path = Path(output_dir)

        # Check if input directory exists
        if not input_path.exists():
            raise typer.BadParameter(f"Input directory '{input_dir}' does not exist")

        # Create output directory if it doesn't exist
        output_path.mkdir(parents=True, exist_ok=True)

        # Initialize chunker
        chunker_config = ChunkerConfig(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        chunker = RecursiveChunker()

        # Initialize embedder
        if embedding_provider == "openai":
            if "OPENAI_API_KEY" not in os.environ:
                raise typer.BadParameter("OpenAI API key is required. Set OPENAI_API_KEY environment variable.")
            embedder = OpenAIEmbedder()
        elif embedding_provider == "huggingface":
            embedder = HuggingFaceEmbedder()
        else:
            raise typer.BadParameter(f"Unsupported embedding provider: {embedding_provider}")

        embedder_config = EmbedderConfig(
            model_name=embedding_model
        )

        # Initialize vector store
        vector_store_config = VectorStoreConfig(
            collection_name="vector-me",
            persist_directory=str(output_path),
            host=qdrant_host,
            port=qdrant_port
        )

        if vector_store == "chroma":
            store = ChromaVectorStore()
        elif vector_store == "faiss":
            store = FAISSVectorStore()
        elif vector_store == "qdrant":
            store = QdrantVectorStore()
        else:
            raise typer.BadParameter(f"Unsupported vector store: {vector_store}")

        # Process files
        print("[bold blue]Processing files...[/bold blue]")
        texts = []
        metadatas = []
        for file_path in input_path.rglob("*"):
            if file_path.is_file():
                try:
                    text = file_path.read_text()
                    chunks = chunker.chunk_text(text, chunker_config)
                    texts.extend(chunks)
                    metadatas.extend([{"source": str(file_path)} for _ in chunks])
                except Exception as e:
                    print(f"[bold red]Error processing {file_path}: {e}[/bold red]")

        if not texts:
            raise typer.BadParameter("No text files found in input directory")

        # Generate embeddings
        print("[bold blue]Generating embeddings...[/bold blue]")
        embeddings = embedder.embed_texts(texts, embedder_config)

        # Store vectors
        print("[bold blue]Storing vectors...[/bold blue]")
        store.add_texts(texts, embeddings, metadatas, vector_store_config)

        # Save FAISS index if using FAISS
        if isinstance(store, FAISSVectorStore):
            store.save(vector_store_config)

        print("[bold green]Vector database built successfully![/bold green]")
        return 0

    except Exception as e:
        print(f"[bold red]Error: {str(e)}[/bold red]")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app() 
# Vector-Me

A flexible vector database builder with plugin support for various chunking strategies, embedding models, and vector stores.

## Features

- Plugin-based architecture for easy extension
- Support for multiple chunking strategies
- Multiple embedding model providers (OpenAI, HuggingFace)
- Multiple vector store backends (Chroma, FAISS, Qdrant)
- CLI interface for easy usage
- GitHub Action support for automated builds

## Installation

```bash
# Using uv (recommended)
uv pip install vector-me

# Using pip
pip install vector-me
```

## Usage

### Command Line Interface

```bash
# Basic usage
vector-me build /path/to/input/dir /path/to/output/dir

# Advanced usage
vector-me build \
    /path/to/input/dir \
    /path/to/output/dir \
    --chunk-size 1000 \
    --chunk-overlap 200 \
    --embedding-model "text-embedding-ada-002" \
    --embedding-provider "openai" \
    --vector-store "chroma" \
    --api-key "your-api-key" \
    --collection-name "my-collection"
```

### GitHub Action

```yaml
name: Build Vector Database

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    
    - name: Build Vector Database
      uses: your-username/vector-me@v1
      with:
        input_dir: ./docs
        output_dir: ./vector-db
        embedding_model: "text-embedding-ada-002"
        embedding_provider: "openai"
        vector_store: "chroma"
        api_key: ${{ secrets.OPENAI_API_KEY }}
```

## Development

1. Clone the repository:
```bash
git clone https://github.com/your-username/vector-me.git
cd vector-me
```

2. Install development dependencies:
```bash
uv pip install -e ".[dev]"
```

3. Run tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
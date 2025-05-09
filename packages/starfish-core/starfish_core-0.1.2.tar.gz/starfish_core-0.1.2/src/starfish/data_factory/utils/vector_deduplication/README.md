# Vector Deduplication Hooks for Starfish

This module provides vector-based deduplication hooks for Starfish data factory. It allows you to detect and filter duplicate records based on vector similarity of text content.

## Features

- Automatic vector embedding of text content
- Configurable similarity threshold
- Support for OpenAI embeddings or custom embedding functions
- Efficient in-memory vector database
- Thread-safe state management
- Integration with Starfish data factory hooks system

## Basic Usage

```python
from starfish import data_factory
from starfish.data_factory.utils.vector_deduplication import create_deduplication_hook

# Create a deduplication hook
dedup_hook = create_deduplication_hook(
    similarity_threshold=0.9,  # Threshold for considering records as duplicates
    content_key="content"  # Field in records containing text to check
)

# Use the hook with data factory
@data_factory(
    on_record_complete=[dedup_hook],
    initial_state_values={"vector_db": {"embeddings": [], "records": []}}
)
async def generate_content(prompt):
    # Your content generation logic here
    return results
```

## Advanced Configuration

### Using OpenAI Embeddings

```python
from openai import OpenAI

# Create OpenAI embedding function
async def get_openai_embedding(text: str):
    client = OpenAI()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

# Create hook with OpenAI embeddings
dedup_hook = create_deduplication_hook(
    similarity_threshold=0.92,
    embedding_func=get_openai_embedding,
    content_key="answer"
)
```

### Customizing Vector Database

You can customize the vector database by modifying the state structure:

```python
@data_factory(
    on_record_complete=[dedup_hook],
    initial_state_values={
        "vector_db": {
            "embeddings": [],  # List of vector embeddings
            "records": [],     # List of corresponding record metadata
            "config": {        # Optional configuration
                "dimension": 1536,
                "metric": "cosine"
            }
        }
    }
)
```

## Understanding Deduplication Results

When a record is processed by the deduplication hook:

1. If it's unique, it adds these fields to the record:
   - `is_duplicate`: False

2. If it's a duplicate, it adds these fields:
   - `is_duplicate`: True
   - `duplicate_of`: ID or index of the original record
   - `similarity_score`: Value between 0-1 indicating similarity

3. The hook returns a status:
   - `"duplicate"` if any records were duplicates
   - `"completed"` if all records were unique

## Advanced Examples

See the example scripts for more advanced usage:

- `test_deduplication.py` - Basic test of deduplication functionality
- `advanced_deduplication_example.py` - More realistic example with custom embedding logic

## Performance Considerations

- Vector comparison is computationally intensive - consider using approximate nearest neighbor algorithms for large datasets
- OpenAI API calls for embeddings will increase cost and latency
- For production use, consider a dedicated vector database like Pinecone, Chroma, or FAISS 
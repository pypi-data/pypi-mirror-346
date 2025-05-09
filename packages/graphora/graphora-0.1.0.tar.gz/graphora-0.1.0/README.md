# Graphora Client Library

A Python client for interacting with the Graphora API. This library provides a simple and intuitive interface for working with Graphora's graph-based data processing capabilities.
Graphora is a Text to Knowledge Graphs platform that helps you transform unstructured text into powerful knowledge graphs.

## Features

- **Complete API Coverage**: Access all Graphora API endpoints
- **Type Safety**: Fully typed with Pydantic models
- **Async Support**: Efficient handling of long-running operations
- **Minimal Dependencies**: Lightweight with few external dependencies
- **Comprehensive Documentation**: Detailed guides and API references

## Installation

```bash
pip install graphora
```

## Quick Start

```python
from graphora import GraphoraClient

# Initialize client
client = GraphoraClient(
    base_url="https://api.graphora.io",
    api_key="your-api-key"  # Or set GRAPHORA_API_KEY environment variable
)

# Upload an ontology
with open("ontology.yaml", "r") as f:
    ontology_yaml = f.read()
    
ontology_response = client.validate_ontology(ontology_yaml)
ontology_id = ontology_response.id

# Upload documents for processing
transform_response = client.upload_documents(
    ontology_id=ontology_id,
    files=["document1.pdf", "document2.txt"]
)

# Wait for processing to complete
transform_status = client.wait_for_transform(transform_response.id)

# Get the resulting graph
graph = client.get_graph(transform_id=transform_response.id)

# Print nodes and edges
print(f"Nodes: {len(graph.nodes)}")
print(f"Edges: {len(graph.edges)}")

# Start merging the processed data
merge_response = client.start_merge(
    session_id=ontology_id,
    transform_id=transform_response.id
)
```

## Environment Variables

The following environment variables can be used to configure the client:

- `GRAPHORA_API_KEY`: Your Graphora API key
- `GRAPHORA_API_URL`: Custom API URL (overrides environment-based URL)

## Documentation

For detailed documentation, see the [docs directory](./docs) or visit our [official documentation website](https://docs.graphora.io).

## Examples

Check out the [examples directory](./examples) for sample code demonstrating various use cases.

## License

MIT License

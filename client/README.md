# KitchenAI FastAPI Client

This FastAPI application serves as a client for interacting with KitchenAI cookbooks. It provides a user-friendly API interface to access various KitchenAI functionalities, including querying, streaming, hybrid search, multi-modal operations, and custom parsing.

## Features

- Standard and streaming queries
- Hybrid search capabilities
- Multi-modal querying (text and image)
- Custom node parsing for advanced text analysis
- File upload and embedding
- Multi-modal file processing
- Custom parse and embed operations

## Prerequisites

- Python 3.8+
- pip (Python package installer)
- A running KitchenAI cookbook Dapr container

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/kitchenai-fastapi-client.git
   cd kitchenai-fastapi-client
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

Ensure that your KitchenAI cookbook Dapr container is running and accessible. Update the `KitchenClient` configuration in the `get_kitchen_client` function if necessary:

```python
def get_kitchen_client():
    with KitchenClient(app_id="kitchenai", namespace="default") as client:
        yield client
```

## Running the Application

Start the FastAPI server:

```
uvicorn main:app --reload
```

The server will start, typically on `http://127.0.0.1:8000`.

## API Endpoints

### 1. Query
- **URL**: `/query`
- **Method**: POST
- **Body**:
  ```json
  {
    "query": "Your query string here"
  }
  ```

### 2. Streaming Query
- **URL**: `/streaming-query`
- **Method**: POST
- **Body**:
  ```json
  {
    "query": "Your query string here"
  }
  ```
- **Note**: Returns a streaming response

### 3. Hybrid Search
- **URL**: `/hybrid-search`
- **Method**: POST
- **Body**:
  ```json
  {
    "query": "Your search query here"
  }
  ```

### 4. Multi-Modal Query
- **URL**: `/multi-modal-query`
- **Method**: POST
- **Body**:
  ```json
  {
    "query": "Your query string here",
    "image_url": "URL to your image"
  }
  ```

### 5. Custom Node Query
- **URL**: `/custom-node-query`
- **Method**: POST
- **Body**:
  ```json
  {
    "query": "Your query string here"
  }
  ```

### 6. File Upload
- **URL**: `/upload`
- **Method**: POST
- **Body**: Form-data with file

### 7. Multi-Modal Upload
- **URL**: `/multi-modal-upload`
- **Method**: POST
- **Body**: Form-data with file

### 8. Custom Parse Upload
- **URL**: `/custom-parse-upload`
- **Method**: POST
- **Body**: Form-data with file

## Usage Examples

### Using curl

1. Standard Query:
   ```
   curl -X POST "http://localhost:8000/query" -H "Content-Type: application/json" -d '{"query": "What is KitchenAI?"}'
   ```

2. File Upload:
   ```
   curl -X POST "http://localhost:8000/upload" -H "Content-Type: multipart/form-data" -F "file=@/path/to/your/file.txt"
   ```

### Using Python requests

```python
import requests

# Standard Query
response = requests.post("http://localhost:8000/query", json={"query": "What is KitchenAI?"})
print(response.json())

# File Upload
with open('/path/to/your/file.txt', 'rb') as f:
    response = requests.post("http://localhost:8000/upload", files={"file": f})
print(response.json())
```

## Error Handling

The application uses FastAPI's built-in error handling. If an error occurs, it will return an appropriate HTTP status code along with an error message.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact the maintainers at support@kitchenai.com.
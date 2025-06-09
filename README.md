# Secure Video Streaming Backend

A secure video streaming backend built with FastAPI that implements token-based authentication and middleware protection for video streams.

## Features

- 🔒 **Secure Video Streaming**: Token-based authentication for video access
- 🛡️ **Middleware Protection**: Custom middleware for request validation
- 🎥 **Multiple Video Formats**: Support for HLS streaming and YouTube embeds
- 🔑 **JWT Authentication**: Secure token generation and validation
- 🌐 **CORS Enabled**: Cross-origin resource sharing support
- 📁 **Static File Serving**: Secure static file delivery
- ⏱️ **Token Expiration**: Configurable token expiration time

## Installation

### Prerequisites

- Python 3.11+
- Docker (optional)

### Local Installation

1. Clone the repository:

```bash
git clone git@github.com:chistym17/vidstream-backend.git
cd vidstream-backend
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the application:

```bash
uvicorn main:app --reload
```

### Docker Installation

1. Build the Docker image:

```bash
docker build -t video-stream-backend .
```

2. Run the container:

```bash
docker run -p 8000:8000 video-stream-backend
```

## API Endpoints

### Authentication

- `GET /get-token?video_id=<video_id>`
  - Generates a JWT token for video access
  - Token expires in 60 minutes
  - Returns: `{"token": "jwt_token"}`

### Video Streaming

- `GET /stream`
  - Streams video content
  - Requires valid JWT token in query params or Authorization header
  - Protected by middleware

### Other Endpoints

- `GET /`: Health check endpoint
- `GET /static/*`: Static file serving

## Security Features

### Token Middleware

The application implements a custom middleware that:

- Validates JWT tokens for protected routes
- Handles token expiration
- Manages static file access
- Logs request processing time

### Token Generation

```python
# Example token payload
{
    "video_id": "video_id",
    "exp": "expiration_timestamp"
}
```

## Usage Example

1. Get a token for video access:

```bash
curl "http://localhost:8000/get-token?video_id=sample1"
```

2. Access the video stream:

```bash
curl "http://localhost:8000/stream?token=your_jwt_token"
```

## Environment Variables

The application uses the following environment variables:

- `PORT`: Server port (default: 8000)
- `SECRET_KEY`: JWT secret key (default: "87539753467")

## Development

To run the application in development mode with auto-reload:

```bash
uvicorn main:app --reload --port 8000
```


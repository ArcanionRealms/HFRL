# HFRL Backend API

FastAPI backend for the HFRL Integration Hub - Human Feedback Reinforcement Learning Platform.

## 🚀 Features

- **Multi-Provider AI Integration**: Support for OpenAI, Anthropic, Deepseek, and Kimi
- **Feedback Management**: Store and retrieve user feedback for AI responses
- **Analytics**: Track performance metrics and improvement rates
- **Settings Management**: Configure API keys and application settings
- **RESTful API**: Clean REST API with automatic OpenAPI documentation
- **Type Safety**: Full type hints with Pydantic validation
- **Async Support**: Built on FastAPI with async/await support

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py          # Configuration settings
│   ├── schemas.py         # Pydantic models
│   ├── routers/           # API routes
│   │   ├── __init__.py
│   │   ├── models.py      # AI model endpoints
│   │   ├── feedback.py    # Feedback endpoints
│   │   ├── analytics.py   # Analytics endpoints
│   │   └── settings.py    # Settings endpoints
│   └── services/          # Business logic
│       ├── __init__.py
│       ├── ai_service.py      # AI provider integrations
│       ├── feedback_service.py # Feedback management
│       └── analytics_service.py # Analytics calculations
├── main.py                # Application entry point
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables example
└── README.md             # This file
```

## 🛠 Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file** (optional):
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

## 🚀 Running the Server

### Development Mode

Run the server with auto-reload:

```bash
python main.py
```

Or using uvicorn directly:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

### Production Mode

For production, use a production ASGI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 📚 API Documentation

### Endpoints

#### Models

- `POST /api/models/generate` - Generate content using AI models
- `POST /api/models/test-connection` - Test connection to AI provider
- `GET /api/models/providers` - Get list of available providers

#### Feedback

- `POST /api/feedback` - Create new feedback
- `GET /api/feedback` - Get all feedback (with optional filters)
- `GET /api/feedback/{feedback_id}` - Get feedback by ID
- `DELETE /api/feedback/{feedback_id}` - Delete feedback
- `GET /api/feedback/session/{session_id}/average` - Get session average rating

#### Analytics

- `GET /api/analytics` - Get analytics data (with optional filters)
- `POST /api/analytics` - Get analytics data (with request body)

#### Settings

- `GET /api/settings` - Get current settings
- `PUT /api/settings` - Update settings

### Example Requests

#### Generate Content

```bash
curl -X POST "http://localhost:8000/api/models/generate" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your-api-key" \
  -d '{
    "prompt": "Hello, how are you?",
    "provider": "openai",
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 1000
  }'
```

#### Create Feedback

```bash
curl -X POST "http://localhost:8000/api/feedback" \
  -H "Content-Type: application/json" \
  -d '{
    "rating": 5,
    "comments": "Great response!",
    "session_id": "session-123",
    "learning_rate": 0.001
  }'
```

#### Get Analytics

```bash
curl "http://localhost:8000/api/analytics"
```

## 🔧 Configuration

### Environment Variables

You can configure the backend using environment variables or a `.env` file:

- `OPENAI_API_KEY` - OpenAI API key
- `ANTHROPIC_API_KEY` - Anthropic API key
- `DEEPSEEK_API_KEY` - Deepseek API key
- `KIMI_API_KEY` - Kimi API key
- `SECRET_KEY` - Secret key for JWT tokens (change in production)
- `CORS_ORIGINS` - Comma-separated list of allowed origins
- `DATABASE_URL` - Database connection URL (for future use)

### API Keys

API keys can be set in three ways:

1. **Environment variables**: Set in your `.env` file or system environment
2. **API settings endpoint**: Update via `PUT /api/settings`
3. **Request header**: Pass `X-API-Key` header in individual requests

## 🔒 Security

### Implemented Security Features

- **Input Validation**: All inputs validated using Pydantic schemas with length limits
- **CORS Configuration**: Specific origins allowed, configurable via settings
- **Error Handling**: Comprehensive error handling with proper logging
- **Request Logging**: All requests and responses logged with timing
- **Type Safety**: Full type hints throughout the codebase
- **Exception Hierarchy**: Custom exception classes for better error handling

### Security Best Practices

1. **API Keys**: Store in environment variables, never commit to version control
2. **CORS**: Configure allowed origins for production
3. **Rate Limiting**: Implement rate limiting (configured but needs middleware)
4. **HTTPS**: Use HTTPS in production
5. **Database**: Use secure database with encrypted connections
6. **Authentication**: Implement JWT or OAuth2 for production
7. **Secrets**: Use strong SECRET_KEY, rotate regularly

## 📊 Data Storage

Currently, the backend uses in-memory storage for feedback and settings. For production:

- Implement a database (PostgreSQL, MySQL, etc.)
- Use SQLAlchemy for database operations
- Add database migrations with Alembic
- Implement proper data persistence

## 🧪 Testing

To test the API:

1. Start the server
2. Visit http://localhost:8000/api/docs for interactive API documentation
3. Use the Swagger UI to test endpoints
4. Or use curl/Postman to make requests

## ✅ Recent Improvements

- ✅ Comprehensive error handling and logging
- ✅ Request/response logging middleware
- ✅ Custom exception hierarchy
- ✅ Input validation with length limits
- ✅ Proper type hints throughout
- ✅ Environment variable configuration
- ✅ .gitignore for security
- ✅ .env.example template

## 🚧 Future Enhancements

- [ ] Database integration (PostgreSQL/SQLite)
- [ ] Authentication and authorization (JWT/OAuth2)
- [ ] Rate limiting middleware implementation
- [ ] Redis caching layer
- [ ] WebSocket support for real-time updates
- [ ] Batch processing for multiple requests
- [ ] Export functionality (CSV, JSON)
- [ ] Prometheus metrics
- [ ] Unit tests with pytest
- [ ] Integration tests
- [ ] Docker containerization
- [ ] CI/CD pipeline

## 📝 License

This project is part of the HFRL Integration Hub.

## 🤝 Contributing

Feedback and suggestions are welcome for future improvements.

---

**HFRL Backend API** - Powered by FastAPI


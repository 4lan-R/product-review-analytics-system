# Product Review Analytics System

A FastAPI-based REST API for analyzing product reviews and performing sentiment analysis with SQLAlchemy ORM and SQLite database.

## Project Structure

```
├── main.py                 # Main FastAPI application
├── database.py             # Database configuration and connection
├── manage_db.py            # Database management utilities
├── requirements.txt        # Project dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore file
├── models/                # SQLAlchemy ORM models
│   ├── __init__.py
│   └── review.py          # Review model
├── schemas/               # Pydantic schemas for validation
│   ├── __init__.py
│   └── review.py          # Review schema definitions
└── routes/                # API route handlers
    ├── __init__.py
    └── reviews.py         # Review endpoints
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables (Optional)

```bash
cp .env.example .env
```

Edit `.env` with your configuration as needed. By default, SQLite database will be created at `./reviews.db`.

### 3. Initialize Database

The database will be automatically initialized when the server starts, but you can manually initialize it:

```bash
python manage_db.py init
```

### 4. Run the Server

```bash
python main.py
```

Or use uvicorn directly:

```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## Database Management

```bash
# Initialize database (create tables)
python manage_db.py init

# Reset database (drop and recreate all tables)
python manage_db.py reset
```

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Reviews

- `GET /api/reviews` - Get all reviews
- `POST /api/reviews` - Create a new review
- `GET /api/reviews/{review_id}` - Get a specific review
- `POST /api/reviews/analyze` - Analyze sentiment of a review

### Health Check

- `GET /health` - Health check endpoint

## Database Schema

### Reviews Table

| Column | Type | Description |
|--------|------|-------------|
| id | String (UUID) | Primary key |
| text | String | Review text |
| product_id | String | Product ID |
| sentiment | String | Sentiment label (positive, negative, neutral) |
| confidence | Float | Confidence score (0.0 - 1.0) |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Technologies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation using Python type annotations
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight SQL database

## Development

To develop further, implement the sentiment analysis logic in `routes/reviews.py` where marked with TODO comments.


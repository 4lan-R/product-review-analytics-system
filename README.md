# Product Review Analytics System

A FastAPI-based REST API for analyzing product reviews and performing sentiment analysis with SQLAlchemy ORM, SQLite database, and Alembic migrations.

## Project Structure

```
├── main.py                 # Main FastAPI application
├── database.py             # Database configuration and connection
├── manage_db.py            # Database management utilities
├── alembic.ini             # Alembic configuration
├── requirements.txt        # Project dependencies
├── .env.example           # Example environment variables
├── .gitignore             # Git ignore file
├── alembic/                # Alembic migrations directory
│   ├── env.py             # Alembic environment script
│   ├── script.py.mako     # Migration template
│   └── versions/          # Migration scripts
│       └── 001_initial.py # Initial migration (create reviews table)
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

### 3. Run Database Migrations

```bash
python manage_db.py migrate
```

This will run all pending migrations and initialize the database schema.

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

### Using Alembic for Migrations

```bash
# Run all pending migrations to latest version (head)
python manage_db.py migrate

# Run migrations to a specific revision
python manage_db.py migrate <revision>

# Downgrade to a previous revision
python manage_db.py downgrade <revision>

# Show current database revision
python manage_db.py current

# Show migration history
python manage_db.py history

# Create a new migration (with autogenerate)
python manage_db.py create '<migration_message>'
```

### Using Direct Database Initialization (Legacy)

```bash
# Initialize database directly (bypass migrations)
python manage_db.py init

# Reset database (drop and recreate all tables)
python manage_db.py reset
```

### Direct Alembic Commands

You can also use Alembic commands directly:

```bash
# Upgrade to latest migration
alembic upgrade head

# Downgrade by one revision
alembic downgrade -1

# Generate automatic migration from model changes
alembic revision --autogenerate -m "Add new column"

# Show current revision
alembic current

# Show revision history
alembic history --oneline
```

## API Documentation

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## API Endpoints

### Review Collection

- `POST /api/reviews/collect` - Collect a scraped review and automatically create the associated product if needed
  - Request body should include review attributes and product information.
  - Example required fields: `title`, `text`, `product_name` or `product_id`
  - Optional product fields: `product_description`
  - Example review fields: `color`, `storage_size`, `rating`, `verified_purchase`

### Review Retrieval (Search)

- `GET /api/reviews/search?color=<color>&storage_size=<size>&rating=<rating>` - Search and retrieve reviews by attributes
  - Query Parameters (all optional):
    - `color`: Filter by product color (e.g., "Red", "Blue", "Black")
    - `storage_size`: Filter by storage size (e.g., "64GB", "128GB", "256GB")
    - `rating`: Filter by review rating (e.g., 1, 2, 3, 4, 5)
  - Example: `/api/reviews/search?color=Red&rating=5`

### Sentiment Analysis

- `POST /api/reviews/sentiment/analyze` - Analyze sentiment of a given text (without storing)
  - Request body: `{"text": "Great product!"}`
  - Returns: Sentiment analysis result with confidence score
  - Use case: Quick sentiment check without creating a review record

### Health Check

- `GET /health` - Health check endpoint

## Database Schema

### Products Table

| Column | Type | Description |
|--------|------|-------------|
| id | String (UUID) | Primary key |
| name | String | Product name |
| description | String | Product description (optional) |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

### Reviews Table

| Column | Type | Description |
|--------|------|-------------|
| id | String (UUID) | Primary key |
| title | String | Review title |
| text | String | Review text |
| product_id | String | Foreign key referencing `products.id` |
| color | String | Product color (optional) |
| storage_size | String | Product storage variant/size (optional) |
| rating | Integer | Review rating 1-5 (optional) |
| verified_purchase | Boolean | Whether this is a verified purchase (default: False) |
| sentiment | String | Sentiment label (positive, negative, neutral) |
| confidence | Float | Confidence score (0.0 - 1.0) |
| created_at | DateTime | Creation timestamp |
| updated_at | DateTime | Last update timestamp |

## Creating New Migrations

When you modify your SQLAlchemy models, you can create a new migration:

```bash
# Alembic will automatically detect changes and generate migration
python manage_db.py create 'Add rating column to reviews'
```

This will create a new migration file in `alembic/versions/` that you can review before running.

## Technologies

- **FastAPI**: Modern web framework for building APIs
- **Uvicorn**: ASGI server
- **Pydantic**: Data validation using Python type annotations
- **SQLAlchemy**: SQL toolkit and ORM
- **SQLite**: Lightweight SQL database
- **Alembic**: Database migration tool for SQLAlchemy

## API Usage Examples

### Create a Review

```bash
curl -X POST "http://localhost:8000/api/reviews" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Great product for the price",
    "text": "Great product, very satisfied! Works perfectly as described.",
    "product_id": "PROD123",
    "color": "Red",
    "storage_size": "128GB",
    "rating": 5,
    "verified_purchase": true
  }'
```

### Search Reviews by Attributes

```bash
# Get all reviews for Red color with 5-star rating
curl "http://localhost:8000/api/reviews/search?color=Red&rating=5"

# Get reviews by storage size
curl "http://localhost:8000/api/reviews/search?storage_size=256GB"

# Combine multiple filters
curl "http://localhost:8000/api/reviews/search?color=Black&storage_size=128GB&rating=4"
```

### Collect Scraped Review

```bash
curl -X POST "http://localhost:8000/api/reviews/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Amazing value for money",
    "text": "This phone has excellent battery life and camera quality.",
    "product_name": "SuperPhone X",
    "product_description": "High-end smartphone with 128GB storage",
    "color": "Blue",
    "storage_size": "128GB",
    "rating": 5,
    "verified_purchase": true
  }'
```

### Analyze Sentiment (Without Storing)

```bash
curl -X POST "http://localhost:8000/api/reviews/sentiment/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "This product is amazing and works perfectly!"
  }'
```

## Development

To develop further, implement the sentiment analysis logic in `routes/reviews.py` where marked with TODO comments.

### Sentiment Analysis Integration

You can integrate with any sentiment analysis library:
- **TextBlob**: Simple, rule-based approach
- **VADER (NLTK)**: Lexicon-based sentiment analysis
- **Hugging Face Transformers**: Deep learning models (RoBERTa, DistilBERT)
- **AWS Comprehend**: Cloud-based API
- **Google Cloud NLP**: Cloud-based API

Example with TextBlob:
```python
from textblob import TextBlob

def analyze_sentiment(text: str):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    
    if polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"
```




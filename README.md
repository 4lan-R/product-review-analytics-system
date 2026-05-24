# Product Review Analytics System

A FastAPI-based REST API for analyzing product reviews and performing sentiment analysis with SQLAlchemy ORM, SQLite database, and Alembic migrations.

## Project Structure

```
├── main.py                 # Main FastAPI application
├── database.py             # Database configuration and connection
├── manage_db.py            # Database management utilities
├── alembic.ini             # Alembic configuration
├── requirements.txt        # Project dependencies
├── .env                    # Example environment variables
├── .gitignore              # Git ignore file
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

- `POST /api/reviews/collect` - Scrape a product page and automatically create the associated product and reviews.

#### Request Body

```json
{
  "link": "https://www.amazon.in/product-review-page-url"
}
```

#### Features

- Scrapes product information
- Extracts product title and description
- Extracts available reviews
- Creates a product record
- Creates associated review records

---

### Review Retrieval (Search)

- `GET /api/reviews/search` - Search and retrieve reviews by attributes.

#### Query Parameters (all optional)

| Parameter | Description |
|------------|------------|
| color | Filter by product color |
| storage_size | Filter by storage size |
| rating | Filter by review rating |

#### Examples

```text
/api/reviews/search?color=Black
```

```text
/api/reviews/search?storage_size=256GB
```

```text
/api/reviews/search?rating=5
```

### Sentiment Analysis

- `POST /api/reviews/analyze/{product_id}`

Analyzes all reviews belonging to a product using VADER sentiment analysis.

Features:
- Classifies each review as Positive, Negative, or Neutral
- Stores sentiment in the database
- Stores confidence score for each review
- Extracts top positive keywords
- Extracts top negative keywords

Example Response:

```json
{
  "product_id": "2cba5d7c-7de6-4bf6-8363-fe48d92c1b0f",
  "total_reviews": 8,
  "positive_reviews": 7,
  "negative_reviews": 1,
  "neutral_reviews": 0,
  "top_positive_keywords": [
    "camera",
    "battery",
    "display",
    "quality",
    "performance"
  ],
  "top_negative_keywords": [
    "heating",
    "issue",
    "slow"
  ]
}
```

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

- **FastAPI**: REST API development
- **Uvicorn**: ASGI application server
- **Pydantic**: Request/response validation
- **SQLAlchemy**: ORM and database operations
- **SQLite**: Persistent data storage
- **Alembic**: Database migrations
- **Playwright**: Product page scraping and review collection
- **BeautifulSoup4**: HTML parsing and review extraction
- **VADER Sentiment**: Sentiment classification (Positive, Negative, Neutral)
- **Scikit-Learn**: Stopword removal and keyword extraction


## API Usage Examples

### Collect Product Reviews from Amazon

Scrape a product page and automatically create the product and reviews.

```bash
curl -X POST "http://localhost:8000/api/reviews/collect" \
  -H "Content-Type: application/json" \
  -d '{
    "link": "https://www.amazon.in/product-review-page-url"
  }'
```

Example Response:

```json
{
  "id": "2cba5d7c-7de6-4bf6-8363-fe48d92c1b0f",
  "name": "Samsung Galaxy S24",
  "description": "Latest Samsung smartphone...",
  "reviews": [
    {
      "review_title": "Excellent phone",
      "review_text": "Amazing camera and battery life.",
      "rating": 5,
      "verified_purchase": true
    }
  ]
}
```

---

### Search Reviews

Search reviews using optional filters.

#### Filter by Rating

```bash
curl "http://localhost:8000/api/reviews/search?rating=5"
```

#### Filter by Color

```bash
curl "http://localhost:8000/api/reviews/search?color=Black"
```

#### Filter by Storage Size

```bash
curl "http://localhost:8000/api/reviews/search?storage_size=256GB"
```

#### Combine Filters

```bash
curl "http://localhost:8000/api/reviews/search?color=Black&storage_size=256GB&rating=5"
```

Example Response:

```json
[
  {
    "review_title": "Great camera",
    "review_text": "Picture quality is excellent.",
    "rating": 5,
    "verified_purchase": true,
    "color": "Black",
    "storage_size": "256GB"
  }
]
```

---

### Analyze Product Reviews

Analyze all reviews belonging to a product using VADER sentiment analysis.

```bash
curl -X POST "http://localhost:8000/api/reviews/analyze/2cba5d7c-7de6-4bf6-8363-fe48d92c1b0f"
```

Example Response:

```json
{
  "product_id": "2cba5d7c-7de6-4bf6-8363-fe48d92c1b0f",
  "total_reviews": 8,
  "positive_reviews": 7,
  "negative_reviews": 1,
  "neutral_reviews": 0,
  "top_positive_keywords": [
    "camera",
    "battery",
    "display",
    "quality",
    "performance"
  ],
  "top_negative_keywords": [
    "heating",
    "issue",
    "slow"
  ]
}
```

### What Happens During Analysis?

For each review:

- Sentiment is classified as **Positive**, **Negative**, or **Neutral**
- Confidence score is calculated using VADER
- Sentiment and confidence are stored in the database
- Positive and negative keywords are extracted from review text
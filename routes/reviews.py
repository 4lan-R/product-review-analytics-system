"""API routes for review ingestion, sentiment analysis, and retrieval."""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.review import ReviewCreate, Review, AnalysisResult, SentimentAnalysisRequest
from services.review_service import collect_review, search_reviews, analyze_sentiment

router = APIRouter(
    prefix="/api/reviews",
    tags=["reviews"],
    responses={404: {"description": "Not found"}},
)


@router.post("/collect", response_model=Review)
async def collect_review_endpoint(review: ReviewCreate, db: Session = Depends(get_db)):
    """
    Collect a scraped review and automatically create the associated product.

    If the product does not exist, it will be created from the supplied product
    information. This endpoint stores both product and review data together.
    """
    try:
        return collect_review(db, review)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/search", response_model=list[Review])
async def search_reviews_endpoint(
    color: str | None = Query(None),
    storage_size: str | None = Query(None),
    rating: int | None = Query(None),
    db: Session = Depends(get_db),
):
    """
    Search and retrieve reviews by attributes.

    Query Parameters:
    - color: Filter by product color
    - storage_size: Filter by storage size
    - rating: Filter by review rating
    """
    return search_reviews(db, color=color, storage_size=storage_size, rating=rating)


@router.post("/sentiment/analyze", response_model=AnalysisResult)
async def analyze_sentiment_endpoint(
    request: SentimentAnalysisRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze sentiment of a given review text.

    This API performs sentiment analysis on the provided text without
    storing it in the database.
    """
    return analyze_sentiment(request)



"""API routes for review ingestion, sentiment analysis, and retrieval."""
import uuid
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product as ProductModel
from models.review import Review as ReviewModel
from schemas.review import ReviewCreate, Review, AnalysisResult, SentimentAnalysisRequest

router = APIRouter(
    prefix="/api/reviews",
    tags=["reviews"],
    responses={404: {"description": "Not found"}},
)


@router.post("/collect", response_model=Review)
async def collect_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """
    Collect a scraped review and automatically create the associated product.

    If the product does not exist, it will be created from the supplied product
    information. This endpoint stores both product and review data together.
    """
    if not review.product_id and not review.product_name:
        raise HTTPException(
            status_code=400,
            detail="product_id or product_name is required to collect review",
        )

    product = None
    if review.product_id:
        product = db.query(ProductModel).filter(ProductModel.id == review.product_id).first()

    if not product and review.product_name:
        product = db.query(ProductModel).filter(ProductModel.name == review.product_name).first()

    if not product:
        product_id = review.product_id or str(uuid.uuid4())
        product = ProductModel(
            id=product_id,
            name=review.product_name or "Unnamed Product",
            description=review.product_description,
        )
        db.add(product)
        db.commit()
        db.refresh(product)

    db_review = ReviewModel(
        title=review.title,
        text=review.text,
        product_id=product.id,
        color=review.color,
        storage_size=review.storage_size,
        rating=review.rating,
        verified_purchase=review.verified_purchase,
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    # TODO: Implement real sentiment analysis.
    db_review.sentiment = "neutral"
    db_review.confidence = 0.75
    db.commit()
    db.refresh(db_review)

    return db_review


@router.get("/search", response_model=list[Review])
async def search_reviews(
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
    query = db.query(ReviewModel)

    if color:
        query = query.filter(ReviewModel.color == color)
    if storage_size:
        query = query.filter(ReviewModel.storage_size == storage_size)
    if rating:
        query = query.filter(ReviewModel.rating == rating)

    return query.all()


@router.post("/sentiment/analyze", response_model=AnalysisResult)
async def analyze_sentiment(
    request: SentimentAnalysisRequest,
    db: Session = Depends(get_db),
):
    """
    Analyze sentiment of a given review text.

    This API performs sentiment analysis on the provided text without
    storing it in the database.
    """
    # TODO: Replace this placeholder with actual sentiment analysis logic.
    sentiment = "neutral"
    confidence = 0.75

    return {
        "review_id": "sentiment_check",
        "title": "Sentiment Analysis",
        "text": request.text,
        "sentiment": sentiment,
        "confidence": confidence,
    }



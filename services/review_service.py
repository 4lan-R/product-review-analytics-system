"""Business logic for review collection and sentiment analysis."""
import uuid
from typing import Any

from sqlalchemy.orm import Session

from models.product import Product as ProductModel
from models.review import Review as ReviewModel
from schemas.review import ReviewCreate, SentimentAnalysisRequest
from services.review_scraper import scrape_review_from_link


def collect_review(db: Session, review: ReviewCreate) -> ReviewModel:
    """Persist a review and ensure the associated product exists."""
    if not review.product_id and not review.product_name:
        raise ValueError("product_id or product_name is required to collect review")

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


def search_reviews(
    db: Session,
    color: str | None = None,
    storage_size: str | None = None,
    rating: int | None = None,
) -> list[ReviewModel]:
    """Search reviews by optional filter criteria."""
    query = db.query(ReviewModel)

    if color:
        query = query.filter(ReviewModel.color == color)
    if storage_size:
        query = query.filter(ReviewModel.storage_size == storage_size)
    if rating:
        query = query.filter(ReviewModel.rating == rating)

    return query.all()


def collect_review_from_link(db: Session, link: str) -> ReviewModel:
    """Fetch review content from a URL, then persist it as a review."""
    scraped_review = scrape_review_from_link(link)
    return collect_review(db, scraped_review)


def analyze_sentiment(request: SentimentAnalysisRequest) -> dict[str, Any]:
    """Run sentiment analysis on a review text without persisting results."""
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

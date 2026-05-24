"""Business logic for review collection and sentiment analysis."""
import uuid
from typing import Any

from sqlalchemy.orm import Session

from models.product import Product as ProductModel
from models.review import Review as ReviewModel
from schemas.product import ProductResponse
from services.review_scraper import scrape_review_from_link


def collect_review_from_link(db: Session, link: str) -> ProductResponse:
    """Fetch review content from a URL, then persist it as a review."""
    scraped_review = scrape_review_from_link(link)
    return scraped_review


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

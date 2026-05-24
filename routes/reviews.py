"""API routes for review ingestion, sentiment analysis, and retrieval."""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.product import ProductResponse
from schemas.review import ReviewLinkRequest, ReviewBase
from services.review_service import collect_review_from_link, search_reviews

router = APIRouter(
    prefix="/api/reviews",
    tags=["reviews"],
    responses={404: {"description": "Not found"}},
)


@router.post("/collect", response_model=ProductResponse)
async def collect_review_endpoint(
    payload: ReviewLinkRequest,
    db: Session = Depends(get_db),
):
    """
    Collect a review by scraping the provided link and automatically create
    the associated product from extracted page metadata.
    """
    try:
        return await collect_review_from_link(db, str(payload.link))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.get("/search", response_model=list[ReviewBase])
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



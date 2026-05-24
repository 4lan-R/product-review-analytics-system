"""API routes for review ingestion, sentiment analysis, and retrieval."""
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from database import get_db
from schemas.product import ProductResponse
from schemas.review import ReviewLinkRequest, ReviewBase
from services.review_service import collect_review_from_link, search_products, analyze_product_reviews

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
    the associated product and reviews from extracted page metadata.
    """
    try:
        return await collect_review_from_link(db, str(payload.link))
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.get("/search",response_model=list[ProductResponse])
async def search_reviews_endpoint(
    product_id: str | None = Query(None),
    color: str | None = Query(None),
    storage_size: str | None = Query(None),
    rating: int | None = Query(None),
    db: Session = Depends(get_db),
):
    return search_products(
        db,
        product_id=product_id,
        color=color,
        storage_size=storage_size,
        rating=rating,
    )

@router.post("/analyze/{product_id}")
async def analyze_reviews_endpoint(
    product_id: str,
    db: Session = Depends(get_db),
):
    """
    Analyze sentiments for all reviews belonging
    to a specific product.
    """
    try:
        return analyze_product_reviews(
            db,
            product_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

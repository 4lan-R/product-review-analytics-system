"""Business logic for review collection and sentiment analysis."""

from sqlalchemy.orm import Session

from models.product import Product as ProductModel
from models.review import Review as ReviewModel
from schemas.product import ProductResponse
from services.review_scraper import scrape_review_from_link
from services.sentiment_analysis_service import analyze_reviews


async def collect_review_from_link(
    db: Session,
    link: str,
) -> ProductResponse:

    scraped_product = await scrape_review_from_link(link)

    # Create Product
    product = ProductModel(
        name=scraped_product.name,
        description=scraped_product.description,
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    # Create Reviews
    review_objects = []

    for review_data in scraped_product.reviews:
        review = ReviewModel(
            review_title=review_data.review_title,
            review_text=review_data.review_text,
            product_id=product.id,
            color=review_data.color,
            storage_size=review_data.storage_size,
            rating=review_data.rating,
            verified_purchase=review_data.verified_purchase,
        )

        review_objects.append(review)

    db.add_all(review_objects)
    db.commit()

    # Reload product with reviews
    db.refresh(product)

    return ProductResponse(
        id=product.id,
        name=product.name,
        description=product.description,
        reviews=scraped_product.reviews,
    )


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


def analyze_product_reviews(
    db: Session,
    product_id: str,
):
    reviews = (
        db.query(ReviewModel)
        .filter(ReviewModel.product_id == product_id)
        .all()
    )

    if not reviews:
        raise ValueError(
            "No reviews found for this product"
        )

    analysis = analyze_reviews(reviews)

    db.commit()

    return {
        "product_id": product_id,
        "total_reviews": len(reviews),
        "positive_reviews": analysis[
            "positive_count"
        ],
        "negative_reviews": analysis[
            "negative_count"
        ],
        "neutral_reviews": analysis[
            "neutral_count"
        ],
        "top_positive_keywords": analysis[
            "top_positive_keywords"
        ],
        "top_negative_keywords": analysis[
            "top_negative_keywords"
        ],
    }
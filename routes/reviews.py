"""API routes for reviews"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.review import Review as ReviewModel
from schemas.review import ReviewCreate, Review, AnalysisResult

router = APIRouter(
    prefix="/api/reviews",
    tags=["reviews"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Review])
async def get_reviews(db: Session = Depends(get_db)):
    """Get all reviews"""
    reviews = db.query(ReviewModel).all()
    return reviews


@router.post("/", response_model=Review)
async def create_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """Create a new review"""
    db_review = ReviewModel(text=review.text, product_id=review.product_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


@router.get("/{review_id}", response_model=Review)
async def get_review(review_id: str, db: Session = Depends(get_db)):
    """Get a specific review"""
    review = db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.post("/analyze", response_model=AnalysisResult)
async def analyze_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """Analyze sentiment of a review"""
    # Create and save review
    db_review = ReviewModel(text=review.text, product_id=review.product_id)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    
    # TODO: Implement sentiment analysis logic
    db_review.sentiment = "neutral"
    db_review.confidence = 0.75
    db.commit()
    db.refresh(db_review)
    
    return {
        "review_id": db_review.id,
        "text": db_review.text,
        "sentiment": db_review.sentiment,
        "confidence": db_review.confidence
    }


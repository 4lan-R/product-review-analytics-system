"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel
from datetime import datetime


class ReviewBase(BaseModel):
    title: str
    text: str
    product_id: str | None = None
    product_name: str | None = None
    product_description: str | None = None
    color: str | None = None
    storage_size: str | None = None
    rating: int | None = None
    verified_purchase: bool = False


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: str
    sentiment: str
    confidence: float = 0.0
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ReviewQuery(BaseModel):
    """Schema for filtering reviews"""
    color: str | None = None
    storage_size: str | None = None
    rating: int | None = None


class AnalysisResult(BaseModel):
    review_id: str
    title: str
    text: str
    sentiment: str
    confidence: float


class SentimentAnalysisRequest(BaseModel):
    """Request schema for sentiment analysis"""
    text: str




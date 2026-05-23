"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel
from datetime import datetime


class ReviewBase(BaseModel):
    text: str
    product_id: str


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


class AnalysisResult(BaseModel):
    review_id: str
    text: str
    sentiment: str
    confidence: float


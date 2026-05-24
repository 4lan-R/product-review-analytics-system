"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, HttpUrl
from datetime import datetime


class ReviewBase(BaseModel):
    review_title: str
    review_text: str
    product_id: str | None = None
    color: str | None = None
    storage_size: str | None = None
    rating: int | None = None
    verified_purchase: bool = False

class ReviewLinkRequest(BaseModel):
    link: HttpUrl

class ReviewQuery(BaseModel):
    """Schema for filtering reviews"""
    color: str | None = None
    storage_size: str | None = None
    rating: int | None = None



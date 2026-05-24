"""Pydantic schemas for product objects."""
from pydantic import BaseModel
from datetime import datetime
from .review import ReviewBase


class ProductBase(BaseModel):
    name: str
    description: str | None = None

class ProductResponse(ProductBase):
    reviews: list[ReviewBase] = []

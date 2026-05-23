"""Pydantic schemas for product objects."""
from pydantic import BaseModel
from datetime import datetime


class ProductBase(BaseModel):
    name: str
    description: str | None = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

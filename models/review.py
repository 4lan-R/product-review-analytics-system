"""SQLAlchemy ORM models"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float
from database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(String, nullable=False)
    product_id = Column(String, nullable=False)
    sentiment = Column(String, default="neutral")
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Review(id={self.id}, product_id={self.product_id}, sentiment={self.sentiment})>"

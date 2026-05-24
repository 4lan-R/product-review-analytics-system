"""SQLAlchemy ORM models"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Float, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    review_title = Column(String, nullable=False)
    review_text = Column(String, nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=False)
    color = Column(String, nullable=True)
    storage_size = Column(String, nullable=True)
    rating = Column(Integer, nullable=True)
    verified_purchase = Column(Boolean, default=False)
    sentiment = Column(String, default="neutral")
    confidence = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    product = relationship("Product", back_populates="reviews")

    def __repr__(self):
        return f"<Review(id={self.id}, review_title={self.review_title}, product_id={self.product_id}, sentiment={self.sentiment}, rating={self.rating}, verified={self.verified_purchase})>"



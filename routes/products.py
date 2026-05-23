"""API routes for products."""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.product import Product as ProductModel
from schemas.product import ProductCreate, Product

router = APIRouter(
    prefix="/api/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[Product])
async def get_products(db: Session = Depends(get_db)):
    """List all products"""
    return db.query(ProductModel).all()


@router.post("/", response_model=Product)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product"""
    db_product = ProductModel(name=product.name, description=product.description)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: str, db: Session = Depends(get_db)):
    """Get a specific product"""
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

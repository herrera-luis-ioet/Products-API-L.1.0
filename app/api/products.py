from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

from app.models.product import Product
from app.services.product_service import ProductService

router = APIRouter()

class ProductBase(BaseModel):
    """Base product model."""
    name: str 
    description: str
    price: float
    stock_quantity: int
    category: str
    multimedia: List[str]

    class Config:
        from_attributes = True

class ProductCreate(ProductBase):
    """Product creation model."""
    pass

class ProductResponse(ProductBase):
    """Product response model."""
    id: int
    created_at: datetime
    updated_at: datetime

@router.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate, product_service: ProductService = Depends()):
    """
    Create a new product.
    
    - category: Optional product category
    - multimedia: Optional list of media URLs
    - stock_quantity: Product stock level (minimum 0)
    """
    product_dict = product.model_dump()
    product_created= product_service.create_product(product_dict)
    return ProductResponse(**product_created.__dict__)

@router.get("/products/", response_model=List[ProductResponse])
async def get_products(
    product_service: ProductService = Depends()
):
    """
    Get all products with optional filters.
    
    - category: Filter products by category
    - min_stock: Filter products by minimum stock level
    """
    products = product_service.get_all_products()
        
    return [ProductResponse(**product.__dict__) for product in products]

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    product_service: ProductService = Depends()
):
    """Get a product by ID."""
    product = product_service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**product.__dict__)

@router.put("/products/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductCreate,
    product_service: ProductService = Depends()
):
    """
    Update a product.
    
    Supports updating all fields including:
    - category
    - multimedia
    - stock_quantity
    """
    product_dict = product.model_dump()
    updated_product = product_service.update_product(product_id, product_dict)
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return ProductResponse(**updated_product.__dict__)

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int,
    product_service: ProductService = Depends()
):
    """Delete a product."""
    deleted = product_service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

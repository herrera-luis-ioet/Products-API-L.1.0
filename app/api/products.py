from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel, conlist

from app.models.product import Product
from app.services.product_service import ProductService

router = APIRouter()

class ProductCreate(BaseModel):
    """Model for creating a product with validation."""
    name: str
    description: str
    price: float
    category: Optional[str] = None
    multimedia: Optional[conlist(str, min_items=0)] = []  # List of URLs
    stock_quantity: int = 0

    class Config:
        schema_extra = {
            "example": {
                "name": "Sample Product",
                "description": "A detailed product description",
                "price": 29.99,
                "category": "Electronics",
                "multimedia": ["http://example.com/image1.jpg"],
                "stock_quantity": 100
            }
        }

@router.post("/products/", response_model=Product)
async def create_product(product: ProductCreate, product_service: ProductService = Depends()):
    """
    Create a new product.
    
    - category: Optional product category
    - multimedia: Optional list of media URLs
    - stock_quantity: Product stock level (minimum 0)
    """
    product_dict = product.dict()
    return await product_service.create_product(Product(**product_dict))

@router.get("/products/", response_model=List[Product])
async def get_products(
    category: Optional[str] = None,
    min_stock: Optional[int] = None,
    product_service: ProductService = Depends()
):
    """
    Get all products with optional filters.
    
    - category: Filter products by category
    - min_stock: Filter products by minimum stock level
    """
    products = await product_service.get_all_products()
    
    if category:
        products = [p for p in products if p.category == category]
    if min_stock is not None:
        products = [p for p in products if p.stock_quantity >= min_stock]
        
    return products

@router.get("/products/{product_id}", response_model=Product)
async def get_product(product_id: int, product_service: ProductService = Depends()):
    """Get a product by ID."""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=Product)
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
    product_dict = product.dict()
    updated_product = await product_service.update_product(product_id, Product(**product_dict))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{product_id}")
async def delete_product(product_id: int, product_service: ProductService = Depends()):
    """Delete a product."""
    deleted = await product_service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}
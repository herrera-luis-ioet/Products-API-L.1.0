from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from pydantic import BaseModel, Field

from app.models.product import Product
from app.services.product_service import ProductService

router = APIRouter()

class ProductCreate(BaseModel):
    """Model for creating a product with validation."""
    name: str = Field(description="Product name", min_length=1, max_length=100)
    description: str = Field(description="Product description", min_length=10, max_length=1000)
    price: float = Field(gt=0, lt=1000000, description="Product price (greater than 0 and less than 1,000,000)")
    category: Optional[str] = Field(default=None, min_length=2, max_length=50, description="Product category")
    multimedia: Optional[List[str]] = Field(
        default_factory=list,
        max_length=5,
        description="List of media URLs (maximum 5 URLs). Each URL should be a valid string pointing to media content."
    )
    stock_quantity: int = Field(default=0, ge=0, le=100000, description="Product stock quantity (0 to 100,000)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "name": "Sample Product",
                "description": "A detailed product description",
                "price": 29.99,
                "category": "Electronics",
                "multimedia": ["http://example.com/image1.jpg"],
                "stock_quantity": 100
            }
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
    product_dict = product.model_dump()
    return await product_service.create_product(Product(**product_dict))

@router.get("/products/", response_model=List[Product])
async def get_products(
    category: Optional[str] = Field(default=None, description="Filter products by category"),
    min_stock: Optional[int] = Field(default=None, ge=0, description="Filter products by minimum stock level"),
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
async def get_product(
    product_id: int = Field(gt=0, description="Product ID"),
    product_service: ProductService = Depends()
):
    """Get a product by ID."""
    product = await product_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/products/{product_id}", response_model=Product)
async def update_product(
    product_id: int = Field(gt=0, description="Product ID"),
    product: ProductCreate = Field(description="Product data to update"),
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
    updated_product = await product_service.update_product(product_id, Product(**product_dict))
    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated_product

@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int = Field(gt=0, description="Product ID"),
    product_service: ProductService = Depends()
):
    """Delete a product."""
    deleted = await product_service.delete_product(product_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

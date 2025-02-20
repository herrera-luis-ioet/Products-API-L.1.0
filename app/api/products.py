from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, validator
from datetime import datetime

from app.services.product_service import ProductService
from app.repositories.product_repository import ProductRepository
from app.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"description": "Not found"}},
)

# Pydantic models for request/response
class ProductBase(BaseModel):
    """Base Pydantic model for Product data."""
    name: str = Field(..., description="Name of the product", min_length=1)
    description: Optional[str] = Field(None, description="Optional description of the product")
    price: float = Field(..., description="Price of the product", gt=0)

    @validator('price')
    def validate_price(cls, v):
        """Validate that price is positive and has at most 2 decimal places."""
        if round(v, 2) != v:
            raise ValueError('Price must have at most 2 decimal places')
        return v

class ProductCreate(ProductBase):
    """Pydantic model for creating a product."""
    pass

class ProductUpdate(BaseModel):
    """Pydantic model for updating a product."""
    name: Optional[str] = Field(None, description="Name of the product", min_length=1)
    description: Optional[str] = Field(None, description="Optional description of the product")
    price: Optional[float] = Field(None, description="Price of the product", gt=0)

    @validator('price')
    def validate_price(cls, v):
        """Validate that price is positive and has at most 2 decimal places."""
        if v is not None:
            if round(v, 2) != v:
                raise ValueError('Price must have at most 2 decimal places')
        return v

class ProductResponse(ProductBase):
    """Pydantic model for product response."""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

# Dependency injection
def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    """Dependency for getting ProductService instance."""
    repository = ProductRepository(db)
    return ProductService(repository)

# API Routes
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """
    Create a new product.

    Args:
        product (ProductCreate): Product data to create

    Returns:
        ProductResponse: Created product data

    Raises:
        HTTPException: If validation fails or creation fails
    """
    try:
        created_product = service.create_product(product.dict())
        return created_product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get("/", response_model=List[ProductResponse])
async def get_all_products(
    service: ProductService = Depends(get_product_service)
) -> List[ProductResponse]:
    """
    Get all products.

    Returns:
        List[ProductResponse]: List of all products

    Raises:
        HTTPException: If retrieval fails
    """
    try:
        return service.get_all_products()
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """
    Get a specific product by ID.

    Args:
        product_id (int): ID of the product to retrieve

    Returns:
        ProductResponse: Product data

    Raises:
        HTTPException: If product not found or retrieval fails
    """
    try:
        return service.get_product(product_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: int,
    product: ProductUpdate,
    service: ProductService = Depends(get_product_service)
) -> ProductResponse:
    """
    Update a product by ID.

    Args:
        product_id (int): ID of the product to update
        product (ProductUpdate): Product data to update

    Returns:
        ProductResponse: Updated product data

    Raises:
        HTTPException: If product not found or update fails
    """
    try:
        # Only include non-None values in update
        update_data = {k: v for k, v in product.dict().items() if v is not None}
        return service.update_product(product_id, update_data)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    service: ProductService = Depends(get_product_service)
):
    """
    Delete a product by ID.

    Args:
        product_id (int): ID of the product to delete

    Raises:
        HTTPException: If product not found or deletion fails
    """
    try:
        service.delete_product(product_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
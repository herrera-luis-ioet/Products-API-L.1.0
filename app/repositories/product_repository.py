from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.product import Product
from pydantic import BaseModel
from app.database import get_db
from fastapi import Depends


class ProductRepository:
    """
    Repository class for handling all database operations related to the Product model.
    This class implements CRUD operations for products using SQLAlchemy.
    """

    def __init__(self, db: Session = Depends(get_db)):
        """
        Initialize the ProductRepository with a database session.

        Args:
            db (Session): SQLAlchemy database session
        """
        self.db = db

    # PUBLIC_INTERFACE
    def create_product(self, product_data: dict) -> Product:
        """
        Create a new product in the database.

        Args:
            product_data (dict): Dictionary containing product data with keys:
                - name (str): Product name
                - description (str, optional): Product description
                - price (float): Product price
                - category (str, optional): Product category
                - multimedia (list, optional): List of multimedia URLs
                - stock_quantity (int, optional): Available stock quantity

        Returns:
            Product: Created product instance

        Raises:
            ValueError: If required fields are missing or invalid
        """
        if not product_data['name'] or not product_data['price']:
            raise ValueError("Product name and price are required")

        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=float(product_data['price']),
            category=product_data['category'],
            multimedia=product_data['multimedia'],
            stock_quantity=product_data['stock_quantity']
        )
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    # PUBLIC_INTERFACE
    def get_product(self, product_id: int) -> Optional[Product]:
        """
        Retrieve a product by its ID.

        Args:
            product_id (int): ID of the product to retrieve

        Returns:
            Optional[Product]: Product instance if found, None otherwise
        """
        return self.db.query(Product).filter(Product.id == product_id).first()

    # PUBLIC_INTERFACE
    def get_all_products(self) -> List[Product]:
        """
        Retrieve all products from the database.

        Returns:
            List[Product]: List of all products
        """
        return self.db.query(Product).all()

    # PUBLIC_INTERFACE
    def update_product(self, product_id: int, product_data: dict) -> Optional[Product]:
        """
        Update an existing product.

        Args:
            product_id (int): ID of the product to update
            product_data (dict): Dictionary containing product data to update with keys:
                - name (str, optional): Product name
                - description (str, optional): Product description
                - price (float, optional): Product price
                - category (str, optional): Product category
                - multimedia (list, optional): List of multimedia URLs
                - stock_quantity (int, optional): Available stock quantity

        Returns:
            Optional[Product]: Updated product instance if found, None otherwise

        Raises:
            ValueError: If product_data is empty or contains invalid values
        """
        if not product_data:
            raise ValueError("No update data provided")

        product = self.get_product(product_id)
        if not product:
            return None

        if 'name' in product_data:
            product.name = product_data['name']
        if 'description' in product_data:
            product.description = product_data['description']
        if 'price' in product_data:
            product.price = float(product_data['price'])
        if 'category' in product_data:
            product.category = product_data['category']
        if 'multimedia' in product_data:
            product.multimedia = product_data['multimedia']
        if 'stock_quantity' in product_data:
            product.stock_quantity = int(product_data['stock_quantity'])

        self.db.commit()
        self.db.refresh(product)
        return product

    # PUBLIC_INTERFACE
    def delete_product(self, product_id: int) -> bool:
        """
        Delete a product from the database.

        Args:
            product_id (int): ID of the product to delete

        Returns:
            bool: True if product was deleted, False if product was not found
        """
        product = self.get_product(product_id)
        if not product:
            return False

        self.db.delete(product)
        self.db.commit()
        return True

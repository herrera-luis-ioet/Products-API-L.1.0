from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import validates

Base = declarative_base()

class Product(Base):
    """
    Product model representing the products table in the database.
    
    Attributes:
        id (int): Primary key for the product
        name (str): Name of the product
        description (str): Optional description of the product
        price (float): Price of the product
        category (str): Optional category of the product
        multimedia (List[str]): List of multimedia URLs associated with the product
        stock_quantity (int): Current stock quantity of the product
        created_at (datetime): Timestamp when the product was created
        updated_at (datetime): Timestamp when the product was last updated
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String, nullable=True)
    multimedia = Column(ARRAY(String), default=[])
    stock_quantity = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError("Name cannot be empty")
        if len(name) > 100:
            raise ValueError("Name cannot be longer than 100 characters")
        return name

    @validates('price')
    def validate_price(self, key, price):
        if price is None:
            raise ValueError("Price cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price

    @validates('category')
    def validate_category(self, key, category):
        if category and len(category) > 50:
            raise ValueError("Category cannot be longer than 50 characters")
        return category

    @validates('multimedia')
    def validate_multimedia(self, key, multimedia):
        if multimedia is None:
            return []
        if not isinstance(multimedia, list):
            raise ValueError("Multimedia must be a list of strings")
        for url in multimedia:
            if not isinstance(url, str):
                raise ValueError("Multimedia items must be strings")
            if len(url) > 255:
                raise ValueError("Multimedia URL cannot be longer than 255 characters")
        return multimedia

    @validates('stock_quantity')
    def validate_stock_quantity(self, key, quantity):
        if quantity is None:
            return 0
        if not isinstance(quantity, int):
            raise ValueError("Stock quantity must be an integer")
        if quantity < 0:
            raise ValueError("Stock quantity cannot be negative")
        return quantity

    def __repr__(self):
        """String representation of the Product model."""
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"

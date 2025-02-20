from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Product(Base):
    """
    Product model representing the products table in the database.
    
    Attributes:
        id (int): Primary key for the product
        name (str): Name of the product
        description (str): Optional description of the product
        price (float): Price of the product
        created_at (datetime): Timestamp when the product was created
        updated_at (datetime): Timestamp when the product was last updated
    """
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        """String representation of the Product model."""
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
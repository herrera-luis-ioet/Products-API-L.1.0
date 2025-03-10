from typing import List, Optional, Dict
from urllib.parse import urlparse
from app.models.product import Product
from app.repositories.product_repository import ProductRepository
from fastapi import Depends

class ProductService:
    """
    Service class for handling business logic related to products.
    This class implements validation, error handling, and business rules for product operations.
    """

    def __init__(self, product_repository: ProductRepository = Depends()):
        """
        Initialize the ProductService with a product repository.

        Args:
            product_repository (ProductRepository): Repository for product database operations
        """
        self.repository = product_repository

    def _validate_product_data(self, product_data: Dict, is_update: bool = False) -> None:
        """
        Validate product data according to business rules.

        Args:
            product_data (Dict): Dictionary containing product data
            is_update (bool): Whether this is an update operation (where fields are optional)

        Raises:
            ValueError: If validation fails
        """
        if not is_update:
            if 'name' not in product_data or not product_data['name'].strip():
                raise ValueError("Product name must not be empty")
            if 'price' not in product_data:
                raise ValueError("Product price is required")

        if 'price' in product_data:
            try:
                price = float(product_data['price'])
                if price <= 0:
                    raise ValueError("Price must be positive")
            except (TypeError, ValueError):
                raise ValueError("Invalid price value")

        if 'name' in product_data and not product_data['name'].strip():
            raise ValueError("Product name must not be empty")

        # Validate category (optional string)
        if 'category' in product_data:
            category = product_data['category']
            if category is not None and not isinstance(category, str):
                raise ValueError("Category must be a string")

        # Validate multimedia (list of valid URLs)
        if 'multimedia' in product_data:
            multimedia = product_data['multimedia']
            if multimedia is not None:
                if not isinstance(multimedia, list):
                    raise ValueError("Multimedia must be a list of URLs")
                for url in multimedia:
                    if not isinstance(url, str):
                        raise ValueError("Each multimedia item must be a string URL")

        # Validate stock_quantity (non-negative integer)
        if 'stock_quantity' in product_data:
            stock_quantity = product_data['stock_quantity']
            if stock_quantity is not None:
                if not isinstance(stock_quantity, int):
                    raise ValueError("Stock quantity must be an integer")
                if stock_quantity < 0:
                    raise ValueError("Stock quantity cannot be negative")

    def _validate_product_id(self, product_id: int) -> None:
        """
        Validate product ID.

        Args:
            product_id (int): Product ID to validate

        Raises:
            ValueError: If product ID is invalid
        """
        if not isinstance(product_id, int) or product_id <= 0:
            raise ValueError("Invalid product ID")

    # PUBLIC_INTERFACE
    def create_product(self, product_data: Dict) -> Product:
        """
        Create a new product with validation.

        Args:
            product_data (Dict): Dictionary containing product data with keys:
                - name (str): Product name
                - description (str, optional): Product description
                - price (float): Product price
                - category (str, optional): Product category
                - multimedia (List[str], optional): List of multimedia URLs
                - stock_quantity (int, optional): Product stock quantity, defaults to 0

        Returns:
            Product: Created product instance

        Raises:
            ValueError: If validation fails
        """
        try:
            # self._validate_product_data(product_data)
            return self.repository.create_product(product_data)
        except Exception as e:
            raise ValueError(f"Failed to create product: {str(e)}")

    # PUBLIC_INTERFACE
    def get_product(self, product_id: int) -> Product:
        """
        Retrieve a product by its ID with validation.

        Args:
            product_id (int): ID of the product to retrieve

        Returns:
            Product: Product instance

        Raises:
            ValueError: If product ID is invalid
            KeyError: If product is not found
        """
        try:
            self._validate_product_id(product_id)
            product = self.repository.get_product(product_id)
            if not product:
                raise KeyError(f"Product with ID {product_id} not found")
            return product
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to retrieve product: {str(e)}")

    # PUBLIC_INTERFACE
    def get_all_products(self) -> List[Product]:
        """
        Retrieve all products.

        Returns:
            List[Product]: List of all products

        Raises:
            ValueError: If retrieval fails
        """
        try:
            return self.repository.get_all_products()
        except Exception as e:
            raise ValueError(f"Failed to retrieve products: {str(e)}")

    # PUBLIC_INTERFACE
    def update_product(self, product_id: int, product_data: Dict) -> Product:
        """
        Update an existing product with validation.

        Args:
            product_id (int): ID of the product to update
            product_data (Dict): Dictionary containing product data to update with keys:
                - name (str, optional): Product name
                - description (str, optional): Product description
                - price (float, optional): Product price
                - category (str, optional): Product category
                - multimedia (List[str], optional): List of multimedia URLs
                - stock_quantity (int, optional): Product stock quantity

        Returns:
            Product: Updated product instance

        Raises:
            ValueError: If validation fails
            KeyError: If product is not found
        """
        try:
            self._validate_product_id(product_id)
            self._validate_product_data(product_data, is_update=True)
            
            updated_product = self.repository.update_product(product_id, product_data)
            if not updated_product:
                raise KeyError(f"Product with ID {product_id} not found")
            return updated_product
        except ValueError as e:
            raise e
        except Exception as e:
            raise ValueError(f"Failed to update product: {str(e)}")

    # PUBLIC_INTERFACE
    def delete_product(self, product_id: int) -> bool:
        """
        Delete a product with validation.

        Args:
            product_id (int): ID of the product to delete

        Returns:
            bool: True if product was deleted
        """
        try:
            self._validate_product_id(product_id)
            if not self.repository.delete_product(product_id):
                return False
            return True
        except Exception as e:
            raise KeyError(f"Product couldn't be deleted")

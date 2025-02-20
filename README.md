# Project Repository

This is the initial README file for the project.# Products API

A FastAPI-based RESTful API for managing products with SQLite database backend.

## Features

- CRUD operations for products
- Input validation using Pydantic models
- SQLite database with SQLAlchemy ORM
- Automatic API documentation with Swagger UI
- Clean architecture with repository and service patterns
- Product categorization and filtering
- Multimedia support for product images and videos
- Inventory tracking with stock management

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- SQLAlchemy
- Pydantic
- python-dotenv

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Products-API-L.1.0
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Start the application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access:
- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

### Product Fields

The API supports the following fields for each product:

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| id | integer | Unique identifier | Auto-generated |
| name | string | Product name | Required, non-empty |
| description | string | Product description | Optional |
| price | float | Product price | Required, > 0, max 2 decimals |
| category | string | Product category | Optional |
| multimedia | array | List of media URLs | Optional, valid URLs |
| stock_quantity | integer | Available inventory | Required, >= 0 |
| created_at | datetime | Creation timestamp | Auto-generated |
| updated_at | datetime | Last update timestamp | Auto-updated |

### API Endpoints

#### Products

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/products` | Get all products |
| GET | `/products/{product_id}` | Get a specific product |
| POST | `/products` | Create a new product |
| PUT | `/products/{product_id}` | Update a product |
| DELETE | `/products/{product_id}` | Delete a product |

### Request/Response Examples

#### Create Product

Request:
```json
POST /products
{
  "name": "Sample Product",
  "description": "A sample product description",
  "price": 29.99,
  "category": "Electronics",
  "multimedia": ["https://example.com/product-image.jpg"],
  "stock_quantity": 100
}
```

Response:
```json
{
  "id": 1,
  "name": "Sample Product",
  "description": "A sample product description",
  "price": 29.99,
  "category": "Electronics",
  "multimedia": ["https://example.com/product-image.jpg"],
  "stock_quantity": 100,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

#### Get All Products

Response:
```json
[
  {
    "id": 1,
    "name": "Sample Product",
    "description": "A sample product description",
    "price": 29.99,
    "category": "Electronics",
    "multimedia": ["https://example.com/product-image.jpg"],
    "stock_quantity": 100,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

## Data Validation

- Product name must not be empty
- Price must be positive and have at most 2 decimal places
- Description is optional
- Category is optional but must be a string if provided
- Multimedia must be a list of valid URLs if provided
- Stock quantity must be a non-negative integer

## Filtering Capabilities

The API supports filtering products by:
- Category: `GET /products?category=Electronics`
- Price range: `GET /products?min_price=10&max_price=50`
- Stock availability: `GET /products?in_stock=true`

## Project Structure

```
Products-API-L.1.0/
├── app/
│   ├── api/
│   │   └── products.py      # API routes and request/response models
│   ├── models/
│   │   └── product.py       # SQLAlchemy models
│   ├── repositories/
│   │   └── product_repository.py  # Database operations
│   ├── services/
│   │   └── product_service.py     # Business logic
│   ├── database.py          # Database configuration
│   └── main.py             # Application entry point
├── tests/                   # Test files
└── requirements.txt         # Project dependencies
```

## Error Handling

The API uses standard HTTP status codes:
- 200: Successful operation
- 201: Resource created
- 204: Resource deleted
- 400: Bad request (validation error)
- 404: Resource not found
- 500: Internal server error

## Development

To run tests:
```bash
pytest
```

## License

[Add your license information here]

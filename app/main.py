from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .database import init_db
from app.api.products import router as product_router

app = FastAPI(
    title="Products API",
    description="API for managing products",
    version="1.0.0"
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include product router with prefix
app.include_router(product_router, prefix="/api/v1")


# Global exception handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )

@app.on_event("startup")
async def on_startup():
    await init_db()

@app.get("/")
async def root():
    return {
        "message": "Welcome to Products API",
        "version": "1.0.0",
        "docs_url": "/docs"
    }

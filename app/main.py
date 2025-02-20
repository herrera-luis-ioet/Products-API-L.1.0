from fastapi import FastAPI
from .database import engine, Base

app = FastAPI(
    title="Products API",
    description="API for managing products",
    version="1.0.0"
)

# Create database tables
Base.metadata.create_all(bind=engine)

@app.get("/")
async def root():
    return {"message": "Welcome to Products API"}
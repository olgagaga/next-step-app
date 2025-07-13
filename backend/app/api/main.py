"""
Main FastAPI application for the Next Step App backend.
This file creates the FastAPI app and includes all the routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

# Import our routers (we'll create these next)
from .routers import articles, scheduler, health

# Create the FastAPI application
app = FastAPI(
    title="Next Step App API",
    description="API for scraping and managing UK immigration news",
    version="1.0.0",
    docs_url="/docs",  # Swagger UI documentation
    redoc_url="/redoc"  # ReDoc documentation
)

# Add CORS middleware to allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include our API routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(articles.router, prefix="/api/v1", tags=["articles"])
app.include_router(scheduler.router, prefix="/api/v1", tags=["scheduler"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint that provides basic API information."""
    return {
        "message": "Welcome to Next Step App API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

# Run the application
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (development only)
        log_level="info"
    ) 
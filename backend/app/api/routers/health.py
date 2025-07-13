"""
Health check router for API monitoring.
This router provides endpoints to check if the API is running properly.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..schemas import HealthCheck

router = APIRouter()

@router.get("/health", response_model=HealthCheck)
async def health_check(db: Session = Depends(get_db)):
    """
    Health check endpoint to verify API and database connectivity.
    
    Returns:
        HealthCheck: Status information about the API
    """
    try:
        # Test database connection
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception as e:
        database_status = f"error: {str(e)}"
    
    return HealthCheck(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0",
        database=database_status
    )

@router.get("/health/simple")
async def simple_health_check():
    """
    Simple health check without database dependency.
    
    Returns:
        dict: Simple status message
    """
    return {"status": "ok", "timestamp": datetime.utcnow()} 
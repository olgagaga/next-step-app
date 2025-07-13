#!/usr/bin/env python3
"""
FastAPI server startup script.
This script runs the FastAPI application with proper configuration.
"""

import uvicorn
import sys
from pathlib import Path

# Add the app directory to Python path
sys.path.append(str(Path(__file__).parent / "app"))

if __name__ == "__main__":
    print("Starting Next Step App API server...")
    print("API Documentation will be available at:")
    print("  - Swagger UI: http://localhost:8000/docs")
    print("  - ReDoc: http://localhost:8000/redoc")
    print("  - Health Check: http://localhost:8000/api/v1/health")
    print()
    
    uvicorn.run(
        "app.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        log_level="info",
        access_log=True
    ) 
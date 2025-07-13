"""
Scheduler router for managing the scraping scheduler.
This router provides endpoints to control and monitor the scheduler.
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
import sys
from pathlib import Path

# Add the parent directory to the path so we can import the scheduler
sys.path.append(str(Path(__file__).parent.parent.parent))

from ..database import get_db
from ..schemas import SchedulerStatus, ScrapingRequest
from scheduler.scheduler import ScrapingScheduler

router = APIRouter()

# Global scheduler instance
scheduler_instance = None

def get_scheduler():
    """Get or create the global scheduler instance."""
    global scheduler_instance
    if scheduler_instance is None:
        scheduler_instance = ScrapingScheduler()
    return scheduler_instance

@router.get("/scheduler/status", response_model=SchedulerStatus)
async def get_scheduler_status():
    """
    Get the current status of the scheduler.
    
    Returns:
        SchedulerStatus: Current scheduler status
    """
    scheduler = get_scheduler()
    
    # Get job information
    scheduler.schedule_jobs()
    jobs = scheduler.get_job_info()
    next_run = scheduler.get_next_run()
    
    return SchedulerStatus(
        running=scheduler.running,
        jobs=jobs,
        next_run=next_run['next_run'] if next_run else None
    )

@router.post("/scheduler/start")
async def start_scheduler():
    """
    Start the scheduler.
    
    Returns:
        dict: Status message
    """
    scheduler = get_scheduler()
    
    if scheduler.running:
        raise HTTPException(status_code=400, detail="Scheduler is already running")
    
    scheduler.start()
    return {"message": "Scheduler started successfully"}

@router.post("/scheduler/stop")
async def stop_scheduler():
    """
    Stop the scheduler.
    
    Returns:
        dict: Status message
    """
    scheduler = get_scheduler()
    
    if not scheduler.running:
        raise HTTPException(status_code=400, detail="Scheduler is not running")
    
    scheduler.stop()
    return {"message": "Scheduler stopped successfully"}

@router.post("/scheduler/restart")
async def restart_scheduler():
    """
    Restart the scheduler.
    
    Returns:
        dict: Status message
    """
    scheduler = get_scheduler()
    
    if scheduler.running:
        scheduler.stop()
    
    scheduler.start()
    return {"message": "Scheduler restarted successfully"}

@router.post("/scheduler/run-once")
async def run_scraping_once(
    request: ScrapingRequest,
    background_tasks: BackgroundTasks
):
    """
    Run scraping once manually.
    
    Args:
        request: Scraping request parameters
        background_tasks: FastAPI background tasks
    
    Returns:
        dict: Status message
    """
    scheduler = get_scheduler()
    
    # Run scraping in background to avoid blocking the API
    background_tasks.add_task(
        scheduler.run_scraping_task,
        days_back=request.days_back
    )
    
    return {
        "message": f"Scraping task started (days_back: {request.days_back})",
        "task_id": f"scraping_{datetime.utcnow().isoformat()}"
    }

@router.get("/scheduler/configs")
async def get_available_configs():
    """
    Get available scheduler configurations.
    
    Returns:
        dict: Available configurations
    """
    configs = {
        'default': 'Default configuration (daily at 9 AM)',
        'daily': 'Daily only (daily at 8 AM)',
        'frequent': 'Frequent monitoring (daily + hourly + every 30 min)',
        'business': 'Business hours (daily + every 4 hours)',
        'test': 'Test configuration (every 2 minutes)'
    }
    
    return {
        "configs": configs,
        "current_config": "default"  # You might want to track this
    }

@router.get("/scheduler/logs")
async def get_scheduler_logs(
    lines: int = 50,
    level: str = "INFO"
):
    """
    Get recent scheduler logs.
    
    Args:
        lines: Number of log lines to return
        level: Log level filter
    
    Returns:
        dict: Recent log entries
    """
    try:
        log_file = Path("scheduler.log")
        if not log_file.exists():
            return {"logs": [], "message": "No log file found"}
        
        with open(log_file, 'r') as f:
            log_lines = f.readlines()
        
        # Get last N lines
        recent_logs = log_lines[-lines:] if len(log_lines) > lines else log_lines
        
        return {
            "logs": recent_logs,
            "total_lines": len(log_lines),
            "returned_lines": len(recent_logs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading logs: {str(e)}") 
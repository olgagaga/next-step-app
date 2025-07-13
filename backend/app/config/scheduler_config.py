"""
Scheduler configuration for scraping tasks.
"""

SCHEDULER_CONFIG = {
    # Default number of days to look back when scraping
    "default_days_back": 3,
    
    # Run scraping on startup
    "run_on_startup": True,
    "startup_days_back": 3,
    
    # Daily scraping configuration
    "daily_scraping": {
        "enabled": True,
        "time": "09:00",  # Run at 9 AM
        "days_back": 3    # Look back 3 days
    },
    
    # Hourly scraping configuration (disabled by default)
    "hourly_scraping": {
        "enabled": False,
        "days_back": 1    # Look back 1 day for hourly runs
    },
    
    # Custom jobs for specific intervals
    "custom_jobs": [
        # Example: Run every 6 hours during business hours
        {
            "enabled": False,
            "interval": "6h",
            "days_back": 2,
            "description": "Every 6 hours"
        },
        # Example: Run every 30 minutes for urgent monitoring
        {
            "enabled": False,
            "interval": "30m",
            "days_back": 1,
            "description": "Every 30 minutes"
        }
    ],
    
    # Logging configuration
    "logging": {
        "level": "INFO",
        "file": "scheduler.log",
        "max_size": "10MB",
        "backup_count": 5
    },
    
    # Error handling
    "error_handling": {
        "max_retries": 3,
        "retry_delay": 300,  # 5 minutes
        "continue_on_error": True
    }
}

# Example configurations for different use cases
DAILY_ONLY_CONFIG = {
    **SCHEDULER_CONFIG,
    "hourly_scraping": {"enabled": False},
    "custom_jobs": [],
    "daily_scraping": {
        "enabled": True,
        "time": "08:00",
        "days_back": 3
    }
}

FREQUENT_MONITORING_CONFIG = {
    **SCHEDULER_CONFIG,
    "daily_scraping": {"enabled": True, "time": "09:00", "days_back": 3},
    "hourly_scraping": {"enabled": True, "days_back": 1},
    "custom_jobs": [
        {
            "enabled": True,
            "interval": "30m",
            "days_back": 1,
            "description": "Every 30 minutes"
        }
    ]
}

BUSINESS_HOURS_CONFIG = {
    **SCHEDULER_CONFIG,
    "daily_scraping": {"enabled": True, "time": "09:00", "days_back": 3},
    "custom_jobs": [
        {
            "enabled": True,
            "interval": "4h",
            "days_back": 2,
            "description": "Every 4 hours during business hours"
        }
    ]
}

TEST_CONFIG = {
    **SCHEDULER_CONFIG,
    "run_on_startup": True,
    "startup_days_back": 3,
    "daily_scraping": {"enabled": False, "time": "09:00", "days_back": 3},
    "hourly_scraping": {"enabled": False, "days_back": 1},
    "custom_jobs": [
        {
            "enabled": True,
            "interval": "2m",
            "days_back": 3,
            "description": "Every 2 minutes for testing"
        }
    ]
} 


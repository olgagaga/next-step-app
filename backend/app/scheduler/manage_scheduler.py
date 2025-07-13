#!/usr/bin/env python3
"""
Management script for the scraping scheduler.
"""
import argparse
import json
import sys
from pathlib import Path
import time
from datetime import datetime

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

# Import after adding to path
try:
    from app.scheduler.scheduler import ScrapingScheduler
    from app.config.scheduler_config import SCHEDULER_CONFIG, DAILY_ONLY_CONFIG, FREQUENT_MONITORING_CONFIG, BUSINESS_HOURS_CONFIG, TEST_CONFIG
except ImportError:
    # Fallback for when running as module
    from scheduler.scheduler import ScrapingScheduler
    from config.scheduler_config import SCHEDULER_CONFIG, DAILY_ONLY_CONFIG, FREQUENT_MONITORING_CONFIG, BUSINESS_HOURS_CONFIG, TEST_CONFIG

def load_config(config_name):
    """Load a predefined configuration."""
    configs = {
        'default': SCHEDULER_CONFIG,
        'daily': DAILY_ONLY_CONFIG,
        'frequent': FREQUENT_MONITORING_CONFIG,
        'business': BUSINESS_HOURS_CONFIG,
        'test': TEST_CONFIG
    }
    return configs.get(config_name, SCHEDULER_CONFIG)

def start_scheduler(config_name='default', custom_config=None):
    """Start the scheduler with specified configuration."""
    print(f"🚀 Starting scheduler with config: {config_name}")
    
    if custom_config:
        with open(custom_config, 'r') as f:
            config = json.load(f)
    else:
        config = load_config(config_name)
    
    scheduler = ScrapingScheduler(config)
    scheduler.start()
    
    print("✅ Scheduler started successfully")
    print("📋 Press Ctrl+C to stop the scheduler")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping scheduler...")
        scheduler.stop()
        print("✅ Scheduler stopped")

def run_once(days_back=3):
    """Run scraping once and exit."""
    print(f"🔄 Running scraping task once (days_back: {days_back})")
    
    scheduler = ScrapingScheduler()
    scheduler.run_scraping_task(days_back=days_back)
    print("✅ Task completed")

def show_status():
    """Show scheduler status and next runs."""
    print("📊 Scheduler Status")
    print("=" * 50)
    
    scheduler = ScrapingScheduler()
    scheduler.schedule_jobs()
    
    jobs = scheduler.get_job_info()
    if not jobs:
        print("❌ No jobs scheduled")
        return
    
    print(f"📋 Found {len(jobs)} scheduled jobs:")
    print()
    
    for i, job in enumerate(jobs, 1):
        print(f"{i}. Function: {job['function']}")
        print(f"   Interval: {job['interval']} {job['unit']}")
        if job['next_run']:
            print(f"   Next run: {job['next_run']}")
            time_until = job['next_run'] - datetime.now()
            if time_until.total_seconds() > 0:
                print(f"   Time until: {time_until}")
        print()

def show_configs():
    """Show available configurations."""
    print("⚙️  Available Configurations")
    print("=" * 50)
    
    configs = {
        'default': 'Default configuration (daily at 9 AM)',
        'daily': 'Daily only (daily at 8 AM)',
        'frequent': 'Frequent monitoring (daily + hourly + every 30 min)',
        'business': 'Business hours (daily + every 4 hours)',
        'test': 'Test configuration (every 2 minutes)'
    }
    
    for name, description in configs.items():
        print(f"📋 {name}: {description}")
    
    print("\n💡 Use --config <name> to specify a configuration")

def create_custom_config():
    """Create a custom configuration file template."""
    template = {
        "default_days_back": 3,
        "run_on_startup": True,
        "startup_days_back": 3,
        "daily_scraping": {
            "enabled": True,
            "time": "09:00",
            "days_back": 3
        },
        "hourly_scraping": {
            "enabled": False,
            "days_back": 1
        },
        "custom_jobs": [
            {
                "enabled": False,
                "interval": "6h",
                "days_back": 2,
                "description": "Every 6 hours"
            }
        ]
    }
    
    filename = f"custom_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(filename, 'w') as f:
        json.dump(template, f, indent=2)
    
    print(f"✅ Created custom config template: {filename}")
    print("📝 Edit this file and use --custom-config to load it")

def main():
    parser = argparse.ArgumentParser(description='Manage the scraping scheduler')
    parser.add_argument('action', choices=['start', 'run-once', 'status', 'configs', 'create-config'],
                       help='Action to perform')
    parser.add_argument('--config', choices=['default', 'daily', 'frequent', 'business', 'test'],
                       default='default', help='Configuration to use')
    parser.add_argument('--custom-config', type=str,
                       help='Path to custom configuration file')
    parser.add_argument('--days', type=int, default=3,
                       help='Number of days back to scrape (for run-once)')
    
    args = parser.parse_args()
    
    if args.action == 'start':
        start_scheduler(args.config, args.custom_config)
    elif args.action == 'run-once':
        run_once(args.days)
    elif args.action == 'status':
        show_status()
    elif args.action == 'configs':
        show_configs()
    elif args.action == 'create-config':
        create_custom_config()

if __name__ == "__main__":
    main() 
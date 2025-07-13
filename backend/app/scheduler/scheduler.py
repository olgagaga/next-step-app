#!/usr/bin/env python3
"""
Scheduler module for running scraping tasks at configurable intervals.
"""
import schedule
import time
import threading
import logging
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

# Add the parent directory to the path so we can import from app
sys.path.append(str(Path(__file__).parent.parent))

# Import after adding to path
try:
    from app.scrapper.scrape_uk import fetch_and_store
    from app.config.scheduler_config import SCHEDULER_CONFIG
except ImportError:
    # Fallback for when running as module
    from scrapper.scrape_uk import fetch_and_store
    from config.scheduler_config import SCHEDULER_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ScrapingScheduler:
    """Scheduler for running scraping tasks at configurable intervals."""
    
    def __init__(self, config=None):
        self.config = config or SCHEDULER_CONFIG
        self.running = False
        self.thread = None
        
    def run_scraping_task(self, days_back=None):
        """Run the scraping task with error handling."""
        try:
            logger.info(f"🔄 Starting scheduled scraping task (days_back: {days_back})")
            start_time = datetime.now()
            
            # Run the scraping task
            fetch_and_store(days_back or self.config.get('default_days_back', 3))
            
            end_time = datetime.now()
            duration = end_time - start_time
            logger.info(f"✅ Scraping task completed in {duration}")
            
        except Exception as e:
            logger.error(f"❌ Error in scraping task: {e}", exc_info=True)
    
    def schedule_jobs(self):
        """Set up all scheduled jobs based on configuration."""
        # Clear any existing jobs
        schedule.clear()
        
        # Schedule daily scraping
        if self.config.get('daily_scraping', {}).get('enabled', True):
            time_str = self.config['daily_scraping'].get('time', '09:00')
            days_back = self.config['daily_scraping'].get('days_back', 3)
            
            schedule.every().day.at(time_str).do(
                self.run_scraping_task, days_back=days_back
            )
            logger.info(f"📅 Scheduled daily scraping at {time_str} (days_back: {days_back})")
        
        # Schedule hourly scraping (if enabled)
        if self.config.get('hourly_scraping', {}).get('enabled', False):
            days_back = self.config['hourly_scraping'].get('days_back', 1)
            
            schedule.every().hour.do(
                self.run_scraping_task, days_back=days_back
            )
            logger.info(f"⏰ Scheduled hourly scraping (days_back: {days_back})")
        
        # Schedule custom intervals
        for custom_job in self.config.get('custom_jobs', []):
            if custom_job.get('enabled', True):
                interval = custom_job.get('interval', '1h')
                days_back = custom_job.get('days_back', 3)
                
                if interval.endswith('h'):
                    hours = int(interval[:-1])
                    schedule.every(hours).hours.do(
                        self.run_scraping_task, days_back=days_back
                    )
                    logger.info(f"🕐 Scheduled custom job every {hours} hours (days_back: {days_back})")
                elif interval.endswith('m'):
                    minutes = int(interval[:-1])
                    schedule.every(minutes).minutes.do(
                        self.run_scraping_task, days_back=days_back
                    )
                    logger.info(f"⏱️ Scheduled custom job every {minutes} minutes (days_back: {days_back})")
        
        # Run initial scraping if configured
        if self.config.get('run_on_startup', False):
            days_back = self.config.get('startup_days_back', 3)
            logger.info(f"🚀 Running initial scraping on startup (days_back: {days_back})")
            self.run_scraping_task(days_back=days_back)
    
    def run_scheduler(self):
        """Run the scheduler in a loop."""
        self.running = True
        logger.info("🎯 Scheduler started")
        
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("🛑 Scheduler stopped by user")
                self.running = False
            except Exception as e:
                logger.error(f"❌ Error in scheduler loop: {e}", exc_info=True)
                time.sleep(60)  # Wait before retrying
    
    def start(self):
        """Start the scheduler in a separate thread."""
        if self.thread and self.thread.is_alive():
            logger.warning("⚠️ Scheduler is already running")
            return
        
        self.schedule_jobs()
        self.thread = threading.Thread(target=self.run_scheduler, daemon=True)
        self.thread.start()
        logger.info("🚀 Scheduler started in background thread")
    
    def stop(self):
        """Stop the scheduler."""
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("🛑 Scheduler stopped")
    
    def get_next_run(self):
        """Get information about the next scheduled run."""
        if not schedule.jobs:
            return None
        
        next_job = schedule.next_run()
        if next_job:
            return {
                'next_run': next_job,
                'time_until': next_job - datetime.now()
            }
        return None
    
    def get_job_info(self):
        """Get information about all scheduled jobs."""
        jobs_info = []
        for job in schedule.jobs:
            jobs_info.append({
                'function': job.job_func.__name__,
                'next_run': job.next_run,
                'interval': str(job.interval),
                'unit': job.unit
            })
        return jobs_info

def main():
    """Main function to run the scheduler."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Run the scraping scheduler')
    parser.add_argument('--config', type=str, help='Path to scheduler config file')
    parser.add_argument('--run-once', action='store_true', 
                       help='Run scraping once and exit')
    parser.add_argument('--days', type=int, default=3,
                       help='Number of days back to scrape (default: 3)')
    
    args = parser.parse_args()
    
    # Load custom config if provided
    config = None
    if args.config:
        import json
        with open(args.config, 'r') as f:
            config = json.load(f)
    
    scheduler = ScrapingScheduler(config)
    
    if args.run_once:
        # Run once and exit
        logger.info("🔄 Running scraping task once")
        scheduler.run_scraping_task(days_back=args.days)
        logger.info("✅ Task completed, exiting")
    else:
        # Start the scheduler
        try:
            scheduler.start()
            
            # Keep the main thread alive
            while scheduler.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            logger.info("🛑 Received interrupt signal")
            scheduler.stop()

if __name__ == "__main__":
    main() 
# Scraping Scheduler

A configurable scheduler for running scraping tasks at specified intervals.

## Features

- **Configurable intervals**: Daily, hourly, or custom time intervals
- **Multiple configurations**: Predefined configs for different use cases
- **Database integration**: Automatically stores scraped articles in database
- **Error handling**: Robust error handling with retry logic
- **Logging**: Comprehensive logging to file and console
- **Management tools**: Easy start/stop/status commands

## Quick Start

### 1. Install Dependencies

```bash
# Install the schedule library
pip install schedule

# Or update your project dependencies
poetry install
```

### 2. Basic Usage

```bash
# Run scraping once
python scheduler/manage_scheduler.py run-once --days 3

# Start scheduler with default config (daily at 9 AM)
python scheduler/manage_scheduler.py start

# Start with different config
python scheduler/manage_scheduler.py start --config frequent

# Check scheduler status
python scheduler/manage_scheduler.py status

# View available configurations
python scheduler/manage_scheduler.py configs
```

## Configurations

### Default Configuration
- **Daily scraping**: 9:00 AM, looks back 3 days
- **Startup scraping**: Runs immediately when started
- **Error handling**: 3 retries with 5-minute delays

### Available Configurations

1. **default**: Daily at 9 AM (recommended for most use cases)
2. **daily**: Daily at 8 AM only
3. **frequent**: Daily + hourly + every 30 minutes (for urgent monitoring)
4. **business**: Daily + every 4 hours (for business hours monitoring)

### Custom Configuration

Create a custom configuration:

```bash
python scheduler/manage_scheduler.py create-config
```

This creates a template file that you can edit and use:

```bash
python scheduler/manage_scheduler.py start --custom-config custom_config_20250713_143022.json
```

## Configuration Options

```json
{
  "default_days_back": 3,
  "run_on_startup": true,
  "startup_days_back": 3,
  "daily_scraping": {
    "enabled": true,
    "time": "09:00",
    "days_back": 3
  },
  "hourly_scraping": {
    "enabled": false,
    "days_back": 1
  },
  "custom_jobs": [
    {
      "enabled": false,
      "interval": "6h",
      "days_back": 2,
      "description": "Every 6 hours"
    }
  ]
}
```

## System Service

### Install as System Service

1. Copy the service file:
```bash
sudo cp scheduler/next-step-scheduler.service /etc/systemd/system/
```

2. Update the service file with your user and path:
```bash
sudo nano /etc/systemd/system/next-step-scheduler.service
```

3. Enable and start the service:
```bash
sudo systemctl daemon-reload
sudo systemctl enable next-step-scheduler
sudo systemctl start next-step-scheduler
```

### Service Management

```bash
# Check status
sudo systemctl status next-step-scheduler

# View logs
sudo journalctl -u next-step-scheduler -f

# Stop service
sudo systemctl stop next-step-scheduler

# Restart service
sudo systemctl restart next-step-scheduler
```

## Logging

Logs are written to:
- **File**: `scheduler.log` in the working directory
- **Console**: Standard output when running manually
- **System**: Journal when running as system service

## Database Integration

The scheduler automatically:
- Initializes the database if it doesn't exist
- Seeds sources from the config file
- Stores new articles with timestamps
- Avoids duplicate articles

## Error Handling

- **Retry logic**: Up to 3 retries with 5-minute delays
- **Continue on error**: Scheduler continues running even if individual tasks fail
- **Logging**: All errors are logged with full stack traces

## Monitoring

### Check Scheduler Status
```bash
python scheduler/manage_scheduler.py status
```

### View Recent Articles
```bash
python scrapper/view_articles.py --days 7 --limit 20
```

### Monitor Logs
```bash
# View scheduler logs
tail -f scheduler.log

# View system service logs
sudo journalctl -u next-step-scheduler -f
```

## Examples

### Daily Monitoring (Recommended)
```bash
python scheduler/manage_scheduler.py start --config daily
```

### Frequent Updates for Important News
```bash
python scheduler/manage_scheduler.py start --config frequent
```

### Business Hours Monitoring
```bash
python scheduler/manage_scheduler.py start --config business
```

### Custom Schedule
```bash
# Create custom config
python scheduler/manage_scheduler.py create-config

# Edit the generated file
nano custom_config_*.json

# Start with custom config
python scheduler/manage_scheduler.py start --custom-config custom_config_*.json
```

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you're running from the correct directory
2. **Database errors**: Check file permissions for the database file
3. **Network errors**: Verify internet connectivity and source URLs
4. **Permission errors**: Ensure proper file permissions for logs and database

### Debug Mode

Run with verbose logging:
```bash
python -u scheduler/manage_scheduler.py start --config default
```

### Check Database
```bash
# View articles in database
python scrapper/view_articles.py --limit 10

# Check database structure
sqlite3 scraper.db ".schema"
``` 
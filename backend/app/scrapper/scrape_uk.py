#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from datetime import datetime, date, timedelta
from pathlib import Path
import json
import re
import sqlite3
import argparse

# Database configuration
DB_PATH = str(Path(__file__).parent.parent / "data" / "scraper.db")

def initialize_db():
    """Initialize database if it doesn't exist"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sources (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      label TEXT NOT NULL,
      url TEXT NOT NULL UNIQUE,
      type TEXT NOT NULL,
      selector TEXT,
      link_selector TEXT,
      title_selector TEXT,
      subtitle_selector TEXT,
      date_selector TEXT,
      last_scraped TIMESTAMP
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS articles (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      source_id INTEGER NOT NULL REFERENCES sources(id),
      article_url TEXT NOT NULL UNIQUE,
      title TEXT NOT NULL,
      subtitle TEXT,
      date_published DATE,
      date_fetched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
      content TEXT
    );
    """)
    
    conn.commit()
    conn.close()

def get_source_id(cursor, url):
    """Get source ID from database"""
    cursor.execute("SELECT id FROM sources WHERE url = ?", (url,))
    result = cursor.fetchone()
    return result[0] if result else None

def article_exists(cursor, article_url):
    """Check if article already exists in database"""
    cursor.execute("SELECT id FROM articles WHERE article_url = ?", (article_url,))
    return cursor.fetchone() is not None

def add_article(cursor, source_id, article_url, title, subtitle, date_published):
    """Add new article to database"""
    try:
        cursor.execute("""
            INSERT INTO articles (source_id, article_url, title, subtitle, date_published)
            VALUES (?, ?, ?, ?, ?)
        """, (source_id, article_url, title, subtitle, date_published))
        return True
    except sqlite3.IntegrityError:
        # Article already exists
        return False

def parse_date(date_str):
    """Parse date string in various formats"""
    if not date_str:
        return None
        
    date_str_clean = date_str.strip()
    
    try:
        # Format: "11 July 2025" or "11 July 2025 published amendments"
        if re.match(r'\d{1,2}\s+\w+\s+\d{4}', date_str_clean):
            date_match = re.search(r'(\d{1,2}\s+\w+\s+\d{4})', date_str_clean)
            if date_match:
                date_str_clean = date_match.group(1)
                return datetime.strptime(date_str_clean, '%d %B %Y')
        
        # Format: "2025-07-11" (ISO format)
        elif re.match(r'\d{4}-\d{2}-\d{2}', date_str_clean):
            return datetime.fromisoformat(date_str_clean)
        
        # Format: "11/07/2025" (DD/MM/YYYY)
        elif re.match(r'\d{1,2}/\d{1,2}/\d{4}', date_str_clean):
            return datetime.strptime(date_str_clean, '%d/%m/%Y')
            
    except Exception:
        pass
    
    return None

def fetch_and_store(days_back=3):
    """Fetch articles from the last N days and store in database"""
    # Load config
    config_path = Path(__file__).parent.parent / 'config' / 'uk.json'
    with open(config_path, 'r') as f:
        CONFIG = json.load(f)
    
    # Initialize database
    initialize_db()
    
    # Calculate date range
    end_date = date.today()
    start_date = end_date - timedelta(days=days_back)
    
    print(f"🚀 Starting UK scraper - tracking sources from last {days_back} days")
    print("=" * 80)
    print(f"📅 Date range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    print("=" * 80)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    total_new_articles = 0
    
    for i, src in enumerate(CONFIG["updates"], 1):
        src_id, url, sel, link_sel, title_sel, sub_sel, date_sel = (
            i, src['url'], src['selector'], src['link_selector'], 
            src['title_selector'], src['subtitle_selector'], src['date_selector']
        )
        
        print(f"\n🔍 Scraping source: {url}")
        print(f"   Label: {src.get('label', 'No label')}")
        print(f"   Selector: {sel}")
        print(f"   Link selector: {link_sel}")
        print(f"   Title selector: {title_sel}")
        print(f"   Subtitle selector: {sub_sel}")
        print(f"   Date selector: {date_sel}")
        print("-" * 60)
        
        # Skip if essential selectors are missing
        if not sel or not link_sel or not title_sel:
            print("⚠️  Skipping source - missing essential selectors")
            continue
        
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')

            items = soup.select(sel)
            print(f"📊 Found {len(items)} items matching selector '{sel}'")
            
            new_articles_count = 0
            in_range_count = 0
            
            for item in items:
                # Try to find link
                a_tag = item.select_one(link_sel)
                if not a_tag or not a_tag.get('href'):
                    continue

                article_url = urljoin(url, a_tag['href'])
                
                # Check if article already exists
                if article_exists(cursor, article_url):
                    continue
                
                # Try to find title
                title_tag = item.select_one(title_sel)
                title = title_tag.get_text(strip=True) if title_tag else 'No title found'
                
                # Try to find subtitle
                subtitle_tag = item.select_one(sub_sel) if sub_sel else None
                subtitle = subtitle_tag.get_text(strip=True) if subtitle_tag else 'No subtitle'
                
                # Try to find date
                date_tag = item.select_one(date_sel) if date_sel else None
                date_str = date_tag.get_text(strip=True) if date_tag else 'No date'
                
                # Parse date
                date_published = parse_date(date_str)
                
                if date_published:
                    # Check if within date range
                    article_date = date_published.date()
                    if start_date <= article_date <= end_date:
                        in_range_count += 1
                        print(f"\n--- Item {in_range_count} (Date: {article_date}) ---")
                        print(f"🔗 URL: {article_url}")
                        print(f"📰 Title: {title}")
                        print(f"📝 Subtitle: {subtitle}")
                        print(f"📅 Date: {date_published.strftime('%Y-%m-%d')}")
                        
                        # Add to database
                        if add_article(cursor, src_id, article_url, title, subtitle, date_published):
                            new_articles_count += 1
                            total_new_articles += 1
                            print(f"✅ Added new article to database")
                        else:
                            print(f"⚠️  Article already exists in database")
                    else:
                        # Article is outside our date range
                        if article_date < start_date:
                            # Stop processing older articles (assuming they're sorted by date)
                            print(f"📅 Reached articles older than {days_back} days, stopping...")
                            break
                else:
                    print(f"❌ Could not parse date: '{date_str}'")
            
            print(f"\n📈 Summary for {url}:")
            print(f"   Total items found: {len(items)}")
            print(f"   Articles in date range: {in_range_count}")
            print(f"   New articles added: {new_articles_count}")
            
            # Update last_scraped timestamp
            cursor.execute("UPDATE sources SET last_scraped = ? WHERE id = ?", (datetime.utcnow(), src_id))
            
        except requests.RequestException as e:
            print(f"❌ Error fetching {url}: {e}")
        except Exception as e:
            print(f"❌ Unexpected error processing {url}: {e}")
    
    # Commit all changes
    conn.commit()
    conn.close()
    
    print("\n" + "=" * 80)
    print(f"✅ Scraping complete!")
    print(f"📊 Total new articles added: {total_new_articles}")
    print(f"📅 Date range covered: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")

def main():
    parser = argparse.ArgumentParser(description='Scrape UK government sources for recent articles')
    parser.add_argument('--days', type=int, default=3, 
                       help='Number of days back to track (default: 3)')
    parser.add_argument('--config', type=str, default='config/uk.json',
                       help='Path to config file (default: config/uk.json)')
    
    args = parser.parse_args()
    
    # Update config path if specified
    if args.config != 'config/uk.json':
        global CONFIG
        with open(args.config, 'r') as f:
            CONFIG = json.load(f)
    
    fetch_and_store(args.days)

if __name__ == "__main__":
    main()

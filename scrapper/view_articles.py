#!/usr/bin/env python3
import sqlite3
import argparse
from datetime import datetime, timedelta

DB_PATH = 'scraper.db'

def view_articles(days_back=None, limit=None):
    """View articles from database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Build query
    query = """
        SELECT 
            a.id,
            s.label as source,
            a.title,
            a.subtitle,
            a.article_url,
            a.date_published,
            a.date_fetched
        FROM articles a
        JOIN sources s ON a.source_id = s.id
    """
    
    params = []
    where_clauses = []
    
    if days_back:
        cutoff_date = datetime.now().date() - timedelta(days=days_back)
        where_clauses.append("a.date_published >= ?")
        params.append(cutoff_date)
    
    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)
    
    query += " ORDER BY a.date_published DESC, a.date_fetched DESC"
    
    if limit:
        query += " LIMIT ?"
        params.append(limit)
    
    cursor.execute(query, params)
    articles = cursor.fetchall()
    
    if not articles:
        print("📭 No articles found in database")
        if days_back:
            print(f"   (Filtered to last {days_back} days)")
        return
    
    print(f"📰 Found {len(articles)} articles in database")
    if days_back:
        print(f"   (Filtered to last {days_back} days)")
    print("=" * 80)
    
    for article in articles:
        article_id, source, title, subtitle, url, date_published, date_fetched = article
        
        print(f"\n📄 Article ID: {article_id}")
        print(f"📰 Title: {title}")
        if subtitle and subtitle != 'No subtitle':
            print(f"📝 Subtitle: {subtitle}")
        print(f"🔗 URL: {url}")
        print(f"📅 Published: {date_published}")
        print(f"📊 Source: {source}")
        print(f"🕒 Fetched: {date_fetched}")
        print("-" * 60)
    
    conn.close()

def main():
    parser = argparse.ArgumentParser(description='View articles from database')
    parser.add_argument('--days', type=int, 
                       help='Show only articles from last N days')
    parser.add_argument('--limit', type=int, default=50,
                       help='Limit number of articles shown (default: 50)')
    
    args = parser.parse_args()
    
    view_articles(args.days, args.limit)

if __name__ == "__main__":
    main() 
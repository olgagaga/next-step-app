#!/usr/bin/env python3
import sqlite3
import json
import os

DB_PATH = 'scraper.db'

def seed_sources():
    """Seed sources from config file into database"""
    # Load config
    config_path = 'config/uk.json'
    if not os.path.exists(config_path):
        print(f"❌ Config file not found: {config_path}")
        return
    
    with open(config_path, 'r') as f:
        CONFIG = json.load(f)
    
    # Connect to database
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    print("🌱 Seeding sources into database...")
    
    for i, src in enumerate(CONFIG['updates'], 1):
        try:
            cursor.execute("""
                INSERT OR IGNORE INTO sources 
                (id, label, url, type, selector, link_selector, title_selector, subtitle_selector, date_selector)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                i,
                src['label'],
                src['url'],
                src['type'],
                src.get('selector'),
                src.get('link_selector'),
                src.get('title_selector'),
                src.get('subtitle_selector'),
                src.get('date_selector')
            ))
            
            if cursor.rowcount > 0:
                print(f"✅ Inserted source {i}: {src['label']}")
            else:
                print(f"ℹ️  Source {i} already exists: {src['label']}")
                
        except Exception as e:
            print(f"❌ Error inserting source {i}: {e}")
    
    conn.commit()
    conn.close()
    print("✅ Finished seeding sources.")

if __name__ == "__main__":
    seed_sources() 
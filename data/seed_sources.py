#!/usr/bin/env python3
import sqlite3
import json

with open('../config/uk.json', 'r') as f:
    CONFIG = json.load(f)

def seed_sources(db_path='scraper.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    for src in CONFIG['updates']:
        cursor.execute("""
            INSERT OR IGNORE INTO sources 
            (label, url, type, selector, link_selector, title_selector, subtitle_selector, date_selector)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            src['label'],
            src['url'],
            src['type'],
            src.get('selector'),
            src.get('link_selector'),
            src.get('title_selector'),
            src.get('subtitle_selector'),
            src.get('date_selector')
        ))
        if cursor.rowcount:
            print(f"✅ Inserted source: {src['label']}")
        else:
            print(f"ℹ️  Source already exists, skipped: {src['label']}")

    conn.commit()
    conn.close()
    print("✅ Finished seeding sources.")

if __name__ == "__main__":
    seed_sources()

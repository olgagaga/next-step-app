#!/usr/bin/env python3
import sqlite3

def initialize_db(db_path='scraper.db'):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Table: sources
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

    # Table: articles
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

    # (Optional) summary_pages table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS summary_pages (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      label TEXT NOT NULL,
      url TEXT NOT NULL UNIQUE,
      selector TEXT,
      last_fetched TIMESTAMP
    );
    """)

    conn.commit()
    print(f"✅ Initialized database at '{db_path}' with tables: sources, articles, summary_pages.")
    conn.close()

if __name__ == "__main__":
    initialize_db()

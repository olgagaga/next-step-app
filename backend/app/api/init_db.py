"""
Database initialization script.
This script creates the database tables and seeds initial data.
"""

import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from api.database import engine, Base
from api.models import Source, Article
import json

def init_database():
    """Initialize the database by creating all tables."""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")

def seed_sources():
    """Seed the database with initial sources from config."""
    from sqlalchemy.orm import sessionmaker
    from api.database import SessionLocal
    
    db = SessionLocal()
    
    try:
        # Check if sources already exist
        existing_sources = db.query(Source).count()
        if existing_sources > 0:
            print(f"Found {existing_sources} existing sources, skipping seeding.")
            return
        
        # Load sources from config
        config_path = Path(__file__).parent.parent / "config" / "uk.json"
        if not config_path.exists():
            print(f"Config file not found at {config_path}")
            return
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        sources_data = config.get('updates', [])
        
        for source_data in sources_data:
            source = Source(
                label=source_data['label'],
                url=source_data['url'],
                type=source_data['type'],
                selector=source_data.get('selector'),
                link_selector=source_data.get('link_selector'),
                title_selector=source_data.get('title_selector'),
                subtitle_selector=source_data.get('subtitle_selector'),
                date_selector=source_data.get('date_selector')
            )
            db.add(source)
        
        db.commit()
        print(f"Seeded {len(sources_data)} sources successfully!")
        
    except Exception as e:
        print(f"Error seeding sources: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database...")
    init_database()
    seed_sources()
    print("Database initialization complete!") 
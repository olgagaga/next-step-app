"""
SQLAlchemy models for the Next Step App database.
These models define the structure of our database tables.
"""

from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

# Create the base class for all models
Base = declarative_base()

class Source(Base):
    """
    Model representing a news source (like Gov UK, Parliament, etc.)
    """
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    label = Column(String, nullable=False)
    url = Column(String, unique=True, nullable=False)
    type = Column(String, nullable=False)
    selector = Column(String)
    link_selector = Column(String)
    title_selector = Column(String)
    subtitle_selector = Column(String)
    date_selector = Column(String)
    last_scraped = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to articles
    articles = relationship("Article", back_populates="source")

class Article(Base):
    """
    Model representing a scraped article
    """
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    article_url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    subtitle = Column(Text)
    date_published = Column(Date)
    date_fetched = Column(DateTime, default=datetime.utcnow)
    content = Column(Text)
    
    # Relationship to source
    source = relationship("Source", back_populates="articles") 
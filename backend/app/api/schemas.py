"""
Pydantic schemas for API requests and responses.
These schemas define the data structure for API communication.
"""

from pydantic import BaseModel, HttpUrl
from typing import Optional, List
from datetime import datetime, date

# Base schemas
class SourceBase(BaseModel):
    """Base schema for source data"""
    label: str
    url: str
    type: str
    selector: Optional[str] = None
    link_selector: Optional[str] = None
    title_selector: Optional[str] = None
    subtitle_selector: Optional[str] = None
    date_selector: Optional[str] = None

class ArticleBase(BaseModel):
    """Base schema for article data"""
    title: str
    subtitle: Optional[str] = None
    article_url: str
    date_published: Optional[date] = None

# Response schemas
class Source(SourceBase):
    """Schema for source responses"""
    id: int
    last_scraped: Optional[datetime] = None
    
    class Config:
        from_attributes = True  # Allows conversion from SQLAlchemy models

class Article(ArticleBase):
    """Schema for article responses"""
    id: int
    source_id: int
    date_fetched: datetime
    content: Optional[str] = None
    source: Optional[Source] = None
    
    class Config:
        from_attributes = True

# Request schemas
class SourceCreate(SourceBase):
    """Schema for creating a new source"""
    pass

class ArticleCreate(ArticleBase):
    """Schema for creating a new article"""
    source_id: int

# List response schemas
class ArticleList(BaseModel):
    """Schema for list of articles"""
    articles: List[Article]
    total: int
    page: int
    per_page: int

class SourceList(BaseModel):
    """Schema for list of sources"""
    sources: List[Source]
    total: int

# Health check schema
class HealthCheck(BaseModel):
    """Schema for health check response"""
    status: str
    timestamp: datetime
    version: str
    database: str

# Scheduler schemas
class SchedulerStatus(BaseModel):
    """Schema for scheduler status"""
    running: bool
    jobs: List[dict]
    next_run: Optional[datetime] = None

class ScrapingRequest(BaseModel):
    """Schema for manual scraping request"""
    days_back: int = 3
    run_once: bool = True 
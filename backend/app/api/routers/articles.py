"""
Articles router for managing scraped articles.
This router provides endpoints to view, search, and manage articles.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import Optional, List
from datetime import datetime, timedelta
from ..database import get_db
from ..models import Article, Source
from ..schemas import Article as ArticleSchema, ArticleList

router = APIRouter()

@router.get("/articles/recent", response_model=List[ArticleSchema])
async def get_recent_articles(
    limit: int = Query(10, ge=1, le=50, description="Number of recent articles"),
    db: Session = Depends(get_db)
):
    """
    Get the most recent articles.
    
    Args:
        limit: Number of articles to return (max 50)
        db: Database session
    
    Returns:
        List[Article]: List of recent articles
    """
    articles = db.query(Article).order_by(
        desc(Article.date_fetched)
    ).limit(limit).all()
    return [ArticleSchema.model_validate(article.__dict__) for article in articles]

@router.get("/articles/today", response_model=List[ArticleSchema])
async def get_todays_articles(db: Session = Depends(get_db)):
    """
    Get articles published today.
    
    Args:
        db: Database session
    
    Returns:
        List[Article]: List of today's articles
    """
    today = datetime.now().date()
    articles = db.query(Article).filter(
        Article.date_published == today
    ).order_by(desc(Article.date_fetched)).all()
    return [ArticleSchema.model_validate(article.__dict__) for article in articles]

@router.get("/articles/stats")
async def get_article_stats(db: Session = Depends(get_db)):
    """
    Get statistics about articles.
    
    Args:
        db: Database session
    
    Returns:
        dict: Article statistics
    """
    total_articles = db.query(Article).count()
    today = datetime.now().date()
    todays_articles = db.query(Article).filter(
        Article.date_published == today
    ).count()
    
    # Articles by source
    source_stats = db.query(
        Source.label,
        func.count(Article.id).label('count')
    ).join(Article).group_by(Source.label).all()
    
    return {
        "total_articles": total_articles,
        "todays_articles": todays_articles,
        "articles_by_source": [
            {"source": label, "count": count} 
            for label, count in source_stats
        ]
    }

@router.get("/articles", response_model=ArticleList)
async def get_articles(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(20, ge=1, le=100, description="Articles per page"),
    days_back: Optional[int] = Query(None, description="Filter articles from last N days"),
    source_id: Optional[int] = Query(None, description="Filter by source ID"),
    search: Optional[str] = Query(None, description="Search in title and subtitle"),
    db: Session = Depends(get_db)
):
    """
    Get a paginated list of articles with optional filtering.
    
    Args:
        page: Page number (starts from 1)
        per_page: Number of articles per page (max 100)
        days_back: Filter articles from last N days
        source_id: Filter by specific source
        search: Search term for title and subtitle
        db: Database session
    
    Returns:
        ArticleList: Paginated list of articles
    """
    # Build query
    query = db.query(Article).join(Source)
    
    # Apply filters
    if days_back:
        cutoff_date = datetime.now().date() - timedelta(days=days_back)
        query = query.filter(Article.date_published >= cutoff_date)
    
    if source_id:
        query = query.filter(Article.source_id == source_id)
    
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            (Article.title.contains(search_term)) |
            (Article.subtitle.contains(search_term))
        )
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    articles = query.order_by(desc(Article.date_published)).offset(
        (page - 1) * per_page
    ).limit(per_page).all()
    
    return ArticleList(
        articles=articles,
        total=total,
        page=page,
        per_page=per_page
    )

@router.get("/articles/{article_id}", response_model=ArticleSchema)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """
    Get a specific article by ID.
    
    Args:
        article_id: Article ID
        db: Database session
    
    Returns:
        Article: Article details
    
    Raises:
        HTTPException: If article not found
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article 
import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { apiService, Article } from '../services/api';
import './CountryPage.css';

interface CountryData {
  id: string;
  name: string;
  flag: string;
  description: string;
  lastUpdate: string;
  bannerImage: string;
  tags: string[];
}

const CountryPage: React.FC = () => {
  const { countryId } = useParams<{ countryId: string }>();
  const navigate = useNavigate();
  const [articles, setArticles] = useState<Article[]>([]);
  const [countryData, setCountryData] = useState<CountryData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        
        // Fetch country data
        const country = await apiService.getCountryData(countryId || 'uk');
        setCountryData(country);
        
        // Fetch latest 10 articles from the database
        const response = await fetch('http://localhost:8000/api/v1/articles/recent?limit=10');
        if (!response.ok) {
          throw new Error('Failed to fetch articles');
        }
        
        const latestArticles: Article[] = await response.json();
        setArticles(latestArticles);
        
      } catch (err) {
        console.error('Error fetching data:', err);
        setError('Failed to load country data and updates');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [countryId]);

  const handleArticleClick = (article: Article) => {
    // Open the source URL in a new tab
    window.open(article.article_url, '_blank');
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-GB', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    });
  };

  const truncateText = (text: string, maxLength: number = 150) => {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  if (loading) {
    return (
      <div className="country-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading latest updates...</p>
        </div>
      </div>
    );
  }

  if (error || !countryData) {
    return (
      <div className="country-page">
        <div className="error-message">
          <h2>Country not found</h2>
          <p>{error || 'Unable to load country data'}</p>
          <button onClick={() => navigate('/')} className="back-button">
            Back to Home
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="country-page">
      <div className="page-header">
        <button onClick={() => navigate('/')} className="back-button">
          ← Back to Home
        </button>
        <div className="country-info">
          <span className="country-flag-large">{countryData.flag}</span>
          <h1>{countryData.name}</h1>
          <p className="country-description">{countryData.description}</p>
          <div className="country-meta">
            <span className="last-update">Last updated: {formatDate(countryData.lastUpdate)}</span>
            <div className="tags">
              {countryData.tags.map((tag, index) => (
                <span key={index} className="tag">{tag}</span>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="updates-section">
        <div className="section-header">
          <h2>Latest Updates ({articles.length})</h2>
          <p className="section-description">
            Click on any update to read the full article from the source
          </p>
        </div>
        
        {articles.length === 0 ? (
          <div className="no-updates">
            <p>No recent updates available</p>
            <p>Check back later for new immigration news</p>
          </div>
        ) : (
          <div className="updates-list">
            {articles.map((article) => (
              <div 
                key={article.id} 
                className="update-card clickable"
                onClick={() => handleArticleClick(article)}
                title="Click to read full article"
              >
                <div className="update-header">
                  <h3 className="update-title">{article.title}</h3>
                  <div className="update-meta">
                    <span className="update-date">
                      {article.date_published ? formatDate(article.date_published) : 'Recent'}
                    </span>
                    {article.source && (
                      <span className="update-source">{article.source.label}</span>
                    )}
                  </div>
                </div>
                
                {article.subtitle && (
                  <p className="update-subtitle">{article.subtitle}</p>
                )}
                
                {article.content && (
                  <p className="update-content">
                    {truncateText(article.content)}
                  </p>
                )}
                
                <div className="update-footer">
                  <span className="read-more">Read full article →</span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CountryPage; 
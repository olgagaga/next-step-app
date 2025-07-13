import React, { useState, useEffect } from 'react';
import CountryCard from '../components/CountryCard';
import apiService, { CountryData } from '../services/api';
import './Home.css';

const Home: React.FC = () => {
  const [countries, setCountries] = useState<CountryData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchCountries = async () => {
      try {
        setLoading(true);
        setError(null);

        // For now, we only have UK data
        // In the future, this could fetch multiple countries
        const ukData = await apiService.getCountryData('uk');
        
        if (ukData) {
          setCountries([ukData]);
        } else {
          setError('Failed to load country data');
        }
      } catch (err) {
        console.error('Error fetching countries:', err);
        setError('Failed to connect to the server. Please check if the backend is running.');
      } finally {
        setLoading(false);
      }
    };

    fetchCountries();
  }, []);

  if (loading) {
    return (
      <div className="home">
        <div className="hero-section">
          <h1 className="main-title">NextStep</h1>
          <p className="subtitle">Decide where you move next. Monitor latest immigration policy updates across the world.</p>
        </div>
        
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading latest immigration updates...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="home">
        <div className="hero-section">
          <h1 className="main-title">NextStep</h1>
          <p className="subtitle">Decide where you move next. Monitor latest immigration policy updates across the world.</p>
        </div>
        
        <div className="error-container">
          <div className="error-message">
            <h3>⚠️ Connection Error</h3>
            <p>{error}</p>
            <button 
              className="retry-button"
              onClick={() => window.location.reload()}
            >
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="home">
      <div className="hero-section">
        <h1 className="main-title">NextStep</h1>
        <p className="subtitle">Decide where you move next. Monitor latest immigration policy updates across the world.</p>
      </div>
      
      <div className="countries-grid">
        {countries.map((country) => (
          <CountryCard
            key={country.id}
            id={country.id}
            name={country.name}
            flag={country.flag}
            description={country.description}
            lastUpdate={country.lastUpdate}
            bannerImage={country.bannerImage}
            updates={country.updates}
            tags={country.tags}
          />
        ))}
      </div>
    </div>
  );
};

export default Home; 
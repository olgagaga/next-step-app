import React from 'react';
import CountryCard from '../components/CountryCard';
import './Home.css';

const Home: React.FC = () => {
  // Sample country data - you can expand this later
  const countries = [
    {
      id: 'canada',
      name: 'Canada',
      flag: '🇨🇦',
      description: 'Latest immigration updates and policy changes',
      lastUpdate: '2024-07-12'
    }
  ];

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
          />
        ))}
      </div>
    </div>
  );
};

export default Home; 
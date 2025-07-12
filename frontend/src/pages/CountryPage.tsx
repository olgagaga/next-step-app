import React from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import './CountryPage.css';

const CountryPage: React.FC = () => {
  const { countryId } = useParams<{ countryId: string }>();
  const navigate = useNavigate();

  // Sample country data - you can expand this with real data later
  const countryData = {
    uk: {
      name: 'United Kingdom',
      flag: '🇬🇧',
      description: 'Latest immigration updates and policy changes',
      updates: [
        {
          id: 1,
          title: 'New Express Entry Draw Results',
          date: '2024-07-12',
          content: 'Latest Express Entry draw invited 1,500 candidates with minimum CRS score of 485.'
        },
        {
          id: 2,
          title: 'Updated Study Permit Requirements',
          date: '2024-07-10',
          content: 'New requirements for international students applying for study permits in Canada.'
        }
      ]
    }
  };

  const country = countryData[countryId as keyof typeof countryData];

  if (!country) {
    return (
      <div className="country-page">
        <div className="error-message">
          <h2>Country not found</h2>
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
          <span className="country-flag-large">{country.flag}</span>
          <h1>{country.name}</h1>
          <p className="country-description">{country.description}</p>
        </div>
      </div>

      <div className="updates-section">
        <h2>Latest Updates</h2>
        <div className="updates-list">
          {country.updates.map((update) => (
            <div key={update.id} className="update-card">
              <div className="update-header">
                <h3>{update.title}</h3>
                <span className="update-date">{update.date}</span>
              </div>
              <p>{update.content}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CountryPage; 
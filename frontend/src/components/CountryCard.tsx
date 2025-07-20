import React from 'react';
import { useNavigate } from 'react-router-dom';
import './CountryCard.css';

interface CountryCardProps {
  id: string;
  name: string;
  flag: string;
  description: string;
  lastUpdate: string;
  bannerImage: string;
  updates: string[];
  tags: string[];
}

const CountryCard: React.FC<CountryCardProps> = ({ 
  id, 
  name, 
  flag, 
  description, 
  lastUpdate, 
  bannerImage, 
  updates, 
  tags 
}) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/country/${id}`);
  };

  return (
    <div className="country-card" onClick={handleClick}>
      {/* Banner Section - One third of the card */}
      <div className="card-banner">
        <img src={bannerImage} alt={`${name} landscape`} className="banner-image" />
        <div className="flag-overlay">
          <span className="country-flag">{flag}</span>
        </div>
        <div className="name-overlay">
          <h3 className="country-name">{name}</h3>
        </div>
      </div>

      {/* Content Section - Two thirds of the card */}
      <div className="card-content">
        {/* <p className="country-description">{description}</p>
         */}
        {/* Updates Section */}
        <div className="updates-section">
          <h4 className="updates-title">Latest Updates</h4>
          <ul className="updates-list">
            {updates.map((update, index) => (
              <li key={index} className="update-item">
                {update.slice(0, 85)}...
              </li>
            ))}
          </ul>
        </div>

        {/* Tags Section */}
        <div className="tags-section">
          {tags.map((tag, index) => (
            <span key={index} className="tag">
              {tag}
            </span>
          ))}
        </div>

        <div className="card-footer">
          <span className="last-update">Last updated: {lastUpdate}</span>
        </div>
      </div>
    </div>
  );
};

export default CountryCard; 
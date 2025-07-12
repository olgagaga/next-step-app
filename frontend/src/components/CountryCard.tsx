import React from 'react';
import { useNavigate } from 'react-router-dom';
import './CountryCard.css';

interface CountryCardProps {
  id: string;
  name: string;
  flag: string;
  description: string;
  lastUpdate: string;
}

const CountryCard: React.FC<CountryCardProps> = ({ id, name, flag, description, lastUpdate }) => {
  const navigate = useNavigate();

  const handleClick = () => {
    navigate(`/country/${id}`);
  };

  return (
    <div className="country-card" onClick={handleClick}>
      <div className="card-header">
        <span className="country-flag">{flag}</span>
        <h3 className="country-name">{name}</h3>
      </div>
      <p className="country-description">{description}</p>
      <div className="card-footer">
        <span className="last-update">Last updated: {lastUpdate}</span>
      </div>
    </div>
  );
};

export default CountryCard; 
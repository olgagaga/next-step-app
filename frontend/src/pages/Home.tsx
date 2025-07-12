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
      lastUpdate: '2024-07-12',
      bannerImage: 'https://images.unsplash.com/photo-1519832979-6fa011b87667?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=1000&q=80',
      updates: [
        'New Express Entry draw with 1,500 invitations',
        'Updated study permit requirements for 2024',
        'Provincial Nominee Program changes announced'
      ],
      tags: ['Express Entry', 'Study Permit', 'PNP']
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
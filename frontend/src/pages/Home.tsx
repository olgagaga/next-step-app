import React from 'react';
import CountryCard from '../components/CountryCard';
import './Home.css';

const Home: React.FC = () => {
  // Sample country data - you can expand this later
  const countries = [
    {
      id: "uk",
      name: "United Kingdom",
      flag: "🇬🇧",
      description: "Latest immigration updates and policy changes",
      lastUpdate: "2024-07-12",
      bannerImage:
        "https://images.unsplash.com/photo-1512734099960-65a682cbfe2b?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.1.0&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Nnx8bG9uZG9ufGVufDB8MHwwfHx8Mg%3D%3D",
      updates: [
        "New Skilled Worker visa requirements announced",
        "Updated student visa processing times",
        "Brexit immigration policy changes implemented",
      ],
      tags: ["Skilled Worker", "Student Visa", "Brexit"],
    },
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
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './pages/Home';
import CountryPage from './pages/CountryPage';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/country/:countryId" element={<CountryPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

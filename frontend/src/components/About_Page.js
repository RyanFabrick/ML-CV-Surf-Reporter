import React from 'react';

const AboutPage = ({ onNavigate }) => (
  <div className='page-container'>
    <div className="page-header">
      <h1>About</h1>
      <button className="back-button" onClick={() => onNavigate('dashboard')}>
        Back to Dashboard
      </button>
    </div>
    <div className="page-content">
      <h2>About This Website</h2>
      <p>about stuff here</p>
    </div>
  </div>
);

export default AboutPage;
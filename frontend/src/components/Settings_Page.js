import React from 'react';

//setting page
const SettingsPage = ({ onNavigate }) => (
  <div className='page-container'>
    <div className="page-header">
      <h1>Settings</h1>
      <button className="back-button" onClick={() => onNavigate('dashboard')}>
        Back to Dashboard
      </button>
    </div>
    <div className="page-content">
      <h2>Application Settings</h2>
      <p>settings stuff here</p>
    </div>
  </div>
);

export default SettingsPage;
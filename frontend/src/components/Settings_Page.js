import React from 'react';

const SettingsPage = ({ onNavigate, theme, onThemeChange, fontSize, onFontSizeChange }) => (
  <div className='page-container'>
    <div className="page-header">
      <h1>Settings</h1>
      <button className="back-button" onClick={() => onNavigate('dashboard')}>
        Back to Dashboard
      </button>
    </div>
    <div className="page-content">
      <h2>Application Settings</h2>
      
      <div className="settings-section">
        <h3>Theme</h3>
        <div className="setting-item">
          <label className="setting-label">
            Choose Theme
          </label>
          <div className="theme-buttons">
            <button 
              className={`theme-button ${theme === 'dark' ? 'active' : ''}`}
              onClick={() => onThemeChange('dark')}
            >
              Dark Mode
            </button>
            <button 
              className={`theme-button ${theme === 'light' ? 'active' : ''}`}
              onClick={() => onThemeChange('light')}
            >
              Light Mode
            </button>
          </div>
        </div>
        <p className="setting-description">
          Switch between dark and light mode
        </p>
      </div>

      <div className="settings-section">
        <h3>Font Size</h3>
        <div className="setting-item">
          <label htmlFor="font-size-slider" className="setting-label">
            Text Size: {fontSize}%
          </label>
          <div className="slider-container">
            <span className="slider-label">Small</span>
            <input
            type="range"
            id="font-size-slider"
            className="font-size-slider"
            min="80"
            max="150"
            step="10"
            value={fontSize}
            onChange={(e) => onFontSizeChange(parseInt(e.target.value))}
            />
            <span className="slider-label">Large</span>
          </div>
        </div>
        <p className="setting-description">
          Adjust text size for entire application
        </p>
      </div>

      <div className="settings-section">
        <h3>Preview Changes</h3>
        <div className="preview-container">
          <div className="preview-text">
            <h4>Sample Dashboard Text</h4>
            <p>Text will appear like this with current settings</p>
            <div className="preview-metrics">
              <div className="preview-metric">
                <span className="preview-value">2.1</span>
                <span className="preview-label">Wave Height (m) </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
);

export default SettingsPage;
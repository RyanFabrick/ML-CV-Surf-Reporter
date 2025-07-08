import React from 'react';

//setting page
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
          <label htmlFor="theme-toggle" className="setting-label">
            Dark Mode
          </label>
          <div className="toggle-switch">
            <input
            type="checkbox"
            id="theme-toggle"
            className="toggle-input"
            checked={theme === 'dark'}
            onChange={(e) => onThemeChange(e.target.checked ? 'dark' : 'light')}
            />
            <span className="toggle-slider"></span>
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
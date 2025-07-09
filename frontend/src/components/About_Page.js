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
      <p>
        Write stuff here
      </p>
      
      <div className="settings-section">
        <h3>Computer Vision Works</h3>
        <div className="setting-item">
          <div>
            <div className="setting-label">Real-time Surfer Detection</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Computer Vision & Machine Learning Elements</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Stream Processing</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h3>Data Metric Meanings</h3>
        <div className="setting-item">
          <div>
            <div className="setting-label">Wave Height (Hs)</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Peak Period (Tp)</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Wave Direction (Dp)</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Average Period (Ta)</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Zero Crossing Period (Tz)</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Peak PSD</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
      </div>

      <div className="settings-section">
        <h3>Data Sources</h3>
        <div className="setting-item">
          <div>
            <div className="setting-label">write stuff here ocean data</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">write stuff here surfcam data</div>
            <p className="setting-description">
              write stuff here
            </p>
          </div>
        </div>
      </div>

      
      <div className="settings-section">
        <h3>Public GitHub Repository</h3>
        <div className="setting-item">
          <div>
            <div className="setting-label">GitHub Repository Link</div>
            <p className="setting-description">
              repo link here
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>


);

export default AboutPage;
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
        <div className="setting-item">
          <div>
            <div className="setting-label">Computer Vision & Machine Learning Model in Action</div>
            <p className="setting-description">
              <video width="100%" controls>
                <source src="/videos/Example_Video.mp4" type="video/mp4" />
                Your browser does not support the video tag.
              </video>
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
              Signficant wave height is defined as the average height (meters) of the highest 
              one-third of waves. 
              <strong> This gives a good estimate of how big the waves will feel in the lineup for surfers!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Peak Period (Tp)</div>
            <p className="setting-description">
              The peak period is defined as the time interval (seconds) between waves with
              with the highest energy. This indicates the frequency of the dominant wave system. 
              <strong> Longer peak periods typically mean more powerful, cleaner, and better-shaped waves for surfing!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Wave Direction (Dp)</div>
            <p className="setting-description">
              Wave direction is defined as as the directions (degrees tru) from which the peak
              energy waves are coming. 
              <strong> This helps surfers determine whether a particular break will be working based on how swell hits the coastline!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Average Period (Ta)</div>
            <p className="setting-description">
              The average period is defined as a representation of the mean time between all waves in the
              specturm, weighted by energy. It reflects the general energy distribution across all
              wave frequencies. 
              <strong> It gives surfers a sense of overall swell consistency and helps distinguish between mixed swell energy!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Zero Up-Crossing Period (Tz)</div>
            <p className="setting-description">
              Zero up-crossing period is defiend as the average time between upward crossings of the mean sea 
              level by wave crests. 
              <strong> Surfers can use this to gauge wave rhythm and timing. Shorter periods usually mean choppier conditions!</strong>
            </p>
          </div>
        </div>
        <div className="setting-item">
          <div>
            <div className="setting-label">Peak PSD</div>
            <p className="setting-description">
              Peak power spectral density is defined as the highest energy value (m²/Hz) found in the wave spectrum. 
              <strong> Higher PSD means more focused swell energy, often translating into stronger and more surfable waves!</strong>
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
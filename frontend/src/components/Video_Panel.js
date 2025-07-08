import React from 'react';

const VideoPanel = ({ selectedWebcam, videoData, webcamError, analysisStatus }) => {
  return (
    <div className="panel video-panel">
      <div className="panel-header">
        <h2 className="panel-title">Live Computer Vision Surfcam Analysis</h2>
      </div>
      <div className="analysis-grid">
        <div className="metric-card">
          <div className="metric-value">
            {videoData ? videoData.surfer_count : '--'}
          </div>
          <div className="metric-label">Surfers Out</div>
        </div>
        <div className="metric-card">
          <div className="metric-value">
            {videoData && videoData.status === 'online' ? '🟢' : '🔴'}
          </div>
          <div className="metric-label">Stream Status</div>
        </div>
      </div>
      <div className="video-preview">
        {!selectedWebcam ? (
          <div>Select a webcam to view live analysis</div>
        ) : webcamError ? (
          <div className="error">{webcamError}</div>
        ) : videoData && (videoData.status === 'starting' || videoData.status === 'initializing') ? (
          <div className="analysis-loading">
            <h3>Setting up CV/ML Analysis...</h3>
            <ul className="loading-steps">
              <li>Connect to the live surf cam stream</li>
              <li>Initialize ML Computer Vision model</li>
              <li>Begin real-time surfer detection</li>
            </ul>
            <p className="loading-note">Please wait. The analysis will start automatically!</p>
          </div>
        ) : videoData && videoData.status === 'online' ? (
          <div>
            <div>Live analysis active</div>
            <small>Stream: {videoData.location_name}</small>
          </div>
        ) : (
          <div>Initializing video analysis...</div>
        )}
      </div>
    </div>
  );
};

export default VideoPanel;
import React from 'react';
import { getCurrentWaveData } from '../utils/getCurrentWaveData';

const WaveDataPanel = ({ selectedBuoy, data }) => {
  const currentWave = getCurrentWaveData(data);
  
  return (
    <div className="panel wave-panel">
      <div className="panel-header">
        <h2 className="panel-title">Current Wave Conditions</h2>
      </div>
      {!selectedBuoy ? (
        <div className="wave-metrics">
          <div className="wave-metric">
            <div className="wave-metric-label">Select a buoy to view wave data</div>
          </div>
        </div>
      ) : (
        <div className="wave-metrics">
          <div className="wave-metric">
            <div className="wave-metric-label">Wave Height</div>
            <div className="wave-metric-value">
              {currentWave.waveHeight}
              <span className="wave-metric-unit">m</span>
            </div>
          </div>
          <div className="wave-metric">
            <div className="wave-metric-label">Peak Period</div>
            <div className="wave-metric-value">
              {currentWave.peakPeriod}
              <span className="wave-metric-unit">s</span>
            </div>
          </div>
          <div className="wave-metric">
            <div className="wave-metric-label">Direction</div>
            <div className="wave-metric-value">
              {currentWave.waveDirection}
              <span className="wave-metric-unit">°</span>
            </div>
          </div>
          <div className="wave-metric">
            <div className="wave-metric-label">Avg Period</div>
            <div className="wave-metric-value">
              {currentWave.avgPeriod}
              <span className="wave-metric-unit">s</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default WaveDataPanel;
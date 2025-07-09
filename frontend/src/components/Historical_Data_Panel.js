import React from 'react';

const HistoricalDataPanel = ({ selectedBuoy, data, error, onNavigate }) => {
  const handleHelpClick = () => {
    onNavigate('about');
    //delay before auto scroll
    setTimeout(() => {
      const metricsSection = document.getElementById('data-metrics-section');
      if (metricsSection) {
        metricsSection.scrollIntoView({ behavior: 'smooth' });
      }
    }, 100);
  };

  return (
    <div className="panel historical-panel">
      <div className="panel-header">
        <h2 className="panel-title">Historical Wave Data</h2>
        <div 
          className="help-icon"
          title="What do these data metrics mean?"
          onClick={handleHelpClick}
        >
          ?
        </div>
      </div>
      <div className="data-table">
        <table>
          <thead>
            <tr>
              <th>Date and Time</th>
              <th>Wave Height</th>
              <th>Peak Period</th>
              <th>Direction</th>
              <th>Avg Period</th>
              <th>Zero Cross</th>
              <th>Peak PSD</th>
            </tr>
          </thead>
          <tbody>
            {!selectedBuoy ? (
              <tr>
                <td colSpan="7" className="loading">Select a buoy to view historical data</td>
              </tr>
            ) : error ? (
              <tr>
                <td colSpan="7" className="error">Error: {error}</td>
              </tr>
            ) : !data ? (
              <tr>
                <td colSpan="7" className="loading">Loading historical data...</td>
              </tr>
            ) : (
              data.time.map((time, i) => (
                <tr key={i}>
                  <td>{time}</td>
                  <td>{data.waveHs[i]?.toFixed(1) || '--'} m</td>
                  <td>{data.waveTp[i]?.toFixed(1) || '--'} s</td>
                  <td>{data.waveDp[i]?.toFixed(0) || '--'}°</td>
                  <td>{data.waveTa[i]?.toFixed(1) || '--'} s</td>
                  <td>{data.waveTz[i]?.toFixed(1) || '--'} s</td>
                  <td>{data.wavePeakPSD[i]?.toFixed(3) || '--'} m²/Hz</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default HistoricalDataPanel;
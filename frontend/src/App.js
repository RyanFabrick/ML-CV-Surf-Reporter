import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/surfdata')
      .then((res) => res.json())
      .then((json) => {
        if (json.error) {
          setError(json.error);
        } else {
          setData(json);
        }
      })
      .catch((err) => {
        console.error('Fetch error:', err);
        setError('Failed to fetch data');
      });
  }, []);

return (
    <div className="dashboard">
      <div className="title-box">
        <div className="title">Surf Forecast Data</div>
      </div>
      <div className="metrics-box">
        {error && <div className="error">Error: {error}</div>}
        {data &&
          data.time.map((time, i) => (
            <div key={i} className="metric">
              <strong>Time:</strong> {time} <br />
              <strong>Wave Height:</strong> {data.waveHs[i]} meters <br />
              <strong>Peak Period:</strong> {data.waveTp[i]} seconds <br />
              <strong>Peak Direction:</strong> {data.waveDp[i]} degrees <br />
              <strong>Average Period:</strong> {data.waveTa[i]} seconds <br />
              <strong>Mean Zero-Up Crossing Period:</strong> {data.waveTz[i]} seconds <br />
              <strong>Peak Power Spectral Density:</strong> {data.wavePeakPSD[i]} m²/Hz
            </div>
          ))}
      </div>
    </div>
  );
}

export default App;
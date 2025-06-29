//useState -> store and track data
//useEffect -> runs logic after component loads
import React, { useEffect, useState } from 'react';
import './App.css';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from 'recharts';


//uses react state to track data and error
//data -> data from Flask backend
//error -> possible error during fetch
function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  //runs after empty array is ran, after component mounts
  //fetches data from Flask endpoint
  //dtores in data, if error stores error message
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

  //Prepares data for Recharts
  //transforms raw API data into readable Recharts data
  const chartData = data ? prepareChartData(data) : [];

  function prepareChartData(apiData) {
    //creates array of chart points - combines time and wave measurements
    const ChartPoints = apiData.time.map((timeString, index) => {
      //extras just (HH:MM:SS) from full datetime string
      const timeOnly = extractTimeFromString(timeString);

      //creates a data point object from moment in time
      return {
        time: timeOnly, //x-axis
        waveHeight: apiData.waveHs[index], //y-axis
        peakPeriod: apiData.waveTp[index] //y-axis
      };
    });

    //reverse array - older measurments on left side
    return ChartPoints;
  }

function extractTimeFromString(timeString) {
  //splits spaces, takes time, original if no spaces
  return timeString.split(' ')[1] || timeString;
}


//JSK -> html and JS making user interface
//if error shows <div> with error message
//if valid data, loops throgh timestamps and metrics dispalyed
  return (
    <div className="dashboard">
      <div className="title-box">
        <div className="title">Surf Forecast Data</div>
      </div>

      {data && (
        <div className="chart-container">
          <h2 className="wave-chart-title">Wave Height Over Time</h2>
          {/* ResponsiveContainer makes the chart resize with the window */}
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={chartData}>
              {/* CartesianGrid adds the background grid lines */}
              <CartesianGrid strokeDasharray="3 3" />
              {/* XAxis shows the time labels at bottom */}
              <XAxis dataKey="time" />
              {/* YAxis shows the wave height values on left */}
              <YAxis />
              {/* Tooltip shows details when you hover over points */}
              <Tooltip />
              {/* Legend explains what the lines represent */}
              <Legend />
              {/* The actual line that shows wave height data */}
              <Line 
                type="monotone"           // Smooth curved line
                dataKey="waveHeight"     // Which data to plot (from chartData)
                stroke="#156292"         // Line color (your blue theme)
                strokeWidth={3}          // Line thickness
                name="Wave Height (m)"   // Label in legend and tooltip
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}

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
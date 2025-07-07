//useState -> store and track data
//useEffect -> runs logic after component loads
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import './App.css';

//uses react state to track data and error
function App() {
  //data -> data from Flask backend
  const [data, setData] = useState(null);
  //error -> possible error during fetch
  const [error, setError] = useState(null);
  //add state for selected buoy
  const [selectedBuoy, setSelectedBuoy] = useState('');
  //webcam specific state
  const [selectedWebcam, setSelectedWebcam] = useState('');
  const [videoData, setVideoData] = useState(null);
  const [webcamError, setWebcamError] = useState(null);
  const [analysisStatus, setAnalysisStatus] = useState('');
  
  //state for navigation
  const [currentPage, setCurrentPage] = useState('dashboard')
  
  //currently mock buoy data - (tentative update)
  const buoyOptions = [
    { id: '273', name: 'King-Poloa, AS', location: 'Samoan Islands' },
    { id: '157', name: 'Point Sur, CA', location: 'California' },
    { id: '106', name: 'Waimea Bay, HI', location: 'Hawaii' },
    { id: '067', name: 'San Nicolas Island, CA', location: 'Channel Islands' }
  ];

  //webcam options (tentative update, currently malibu only)
  const webcamOptions = [
  {
    id: 'Windansea', 
    name: 'Windansea - La Jolla', 
    location: 'La Jolla, CA',
    status: 'online',
  },

  {
    id: 'Long Beach', 
    name: 'Long Beach - New York', 
    location: 'Long Beach, NY',
    status: 'online',
  },

  {
    id: 'Emerald Isle', 
    name: 'Emerald Isle - North Carolina', 
    location: 'Bogue Banks, NC',
    status: 'online',
  }

];

//navigation handler
const handleNavigation = (page) => {
  setCurrentPage(page);
};

  //function handles buoy selection changes
  const handleBuoyChange = (event) => {
    const newBuoyId = event.target.value;
    setSelectedBuoy(newBuoyId);
    console.log(`Selected Buoy: ${newBuoyId}`);
  };

  // handles webcam selection changes
  const handleWebcamChange = (event) => {
    const newWebcamId = event.target.value;

    //Stops previous analysis if switching webcams
    if (selectedWebcam && selectedWebcam !== newWebcamId) {
      fetch(`http://localhost:5000/api/stop-analysis/${selectedWebcam}`)
        .catch(err => console.log('Error Stopping Previous Analysis:', err));
    }

    setSelectedWebcam(newWebcamId);
    setVideoData(null);
    setWebcamError(null);
    setAnalysisStatus('');
    //data refreshes due to useEffect dependency
    console.log(`Selected Webcam: ${newWebcamId || 'None'}`);
  };

  //runs after empty array is ran, after component mounts
  //fetches data from Flask endpoint
  //stores in data, if error stores error message
  const fetchWaveData = (buoyId) => {

    //does not fetch if no buoy selected
    if (!buoyId) {
      setData(null);
      setError(null);
      return;
    }

    fetch(`http://localhost:5000/api/surfdata?buoy_id=${buoyId}`)
      .then((res) => res.json())
      .then((json) => {
        if (json.error) {
          setError(`Buoy Data Error: ${json.error}`);
          setData(null);
        } else {
          setData(json);
          setError(null);
        }
      })
      .catch((err) => {
        console.error('Wave Data Fetch Error:', err);
        setError('Failed to fetch wave data - check connection');
        setData(null);
      });
  };

  const fetchVideoData = (webcamId) => {
    if (!webcamId) {
      //no webcam selected, clear data
      setVideoData(null);
      setWebcamError(null);
      setAnalysisStatus('');
      return;
    }
    
    fetch(`http://localhost:5000/api/video-analysis?webcam_id=${webcamId}`)
      .then((res) => res.json())
      .then((json) => {
        if (json.error) {
          setWebcamError(`Webcam Error: ${json.error}`);
          setVideoData(null);
          setAnalysisStatus('error');
        } else {
          setVideoData(json);
          setWebcamError(null);
          setAnalysisStatus(json.status);

          //Show status messages
          if (json.status === 'starting') {
            setAnalysisStatus('Starting Analysis...');
          } else if (json.status === 'initializing') {
            setAnalysisStatus('Initializing Analysis...');
          } else if (json.status === 'online') {
            setAnalysisStatus('Live'); 
          } else if (json.status === 'error') {
            setAnalysisStatus('Analysis Error');
          }
        }
      })
      .catch((err) => {
        console.error('Webcam Data Fetch Error:', err);
        setWebcamError('Failed to fetch webcam data');
        setVideoData(null);
        setAnalysisStatus('error');
      });
  };

  useEffect(() => {
    //initial data fetch
    fetchWaveData(selectedBuoy);
    fetchVideoData(selectedWebcam);

    const waveInterval = setInterval(() => {
      fetchWaveData(selectedBuoy);
    }, 180000); // 3 minutes

    const videoInterval = setInterval(() => {
      if (selectedWebcam) {
        fetchVideoData(selectedWebcam);
      }
    }, 5000); // 5 seconds
    
    return () => {
      clearInterval(waveInterval);
      clearInterval(videoInterval);
    };
  }, [selectedBuoy, selectedWebcam]); // rerun when selection changes

  //Prepares data for Recharts
  //transforms raw API data into readable Recharts data
  const chartData = data ? prepareChartData(data) : [];

  function prepareChartData(apiData) {
    //creates array of chart points - combines time and wave measurements
    const ChartPoints = apiData.time.map((timeString, index) => {
      //converts to date object
      const dateObj = new Date(timeString);
      //formats to 12 hr time with am/pm
      const timeOnly = dateObj.toLocaleTimeString([], {
        hour: 'numeric',
        minute: '2-digit',
        hour12: true
      });
      //creates a data point object from moment in time
      return {
        time: timeOnly, //x-axis
        waveHeight: apiData.waveHs[index], //y-axis
        peakPeriod: apiData.waveTp[index] //y-axis
      };
    });
    //reverse array - older measurements on left side
    return ChartPoints;
  }

  function extractTimeFromString(timeString) {
    //splits spaces, takes time, original if no spaces
    return timeString.split(' ')[1] || timeString;
  }

  const getCurrentWaveData = () => {
    if (!data || !data.waveHs || data.waveHs.length === 0) {
      return {
        waveHeight: '--',
        peakPeriod: '--',
        waveDirection: '--',
        avgPeriod: '--'
      };
    }
    
    const latest = data.waveHs.length - 1;
    return {
      waveHeight: data.waveHs[latest]?.toFixed(1) || '--',
      peakPeriod: data.waveTp[latest]?.toFixed(1) || '--',
      waveDirection: data.waveDp[latest]?.toFixed(0) || '--',
      avgPeriod: data.waveTa[latest]?.toFixed(1) || '--'
    };
  };

  const currentWave = getCurrentWaveData();
  
  //setting page
  const SettingsPage = () => (
    <div className='page-container'>
      <div className="page-header">
        <h1>Settings</h1>
        <button className="back-button" onClick={() => handleNavigation('dashboard')}>
          Back to Dashboard
        </button>
      </div>
      <div className="page-content">
        <h2>Application Settings</h2>
        <p>settings stuff here</p>
      </div>
    </div>
  );

  //about page
  const AboutPage = () => (
    <div className='page-container'>
      <div className="page-header">
        <h1>Settings</h1>
        <button className="back-button" onClick={() => handleNavigation('dashboard')}>
          Back to Dashboard
        </button>
      </div>
      <div className="page-content">
        <h2>About This Website</h2>
        <p>about stuff here</p>
      </div>
    </div>
  );

  // Main Dashboard Component
  const DashboardPage = () => (
    <div className="dashboard">
      {/* Video Analysis Panel */}
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

      {/* Current Wave Data Panel */}
      <div className="panel wave-panel">
        <div className="panel-header">
          <h2 className="panel-title">Current Wave Conditions</h2>
        </div>
        {! selectedBuoy ? (
          <div className="wave-metrics">
            <div className="wave-metric">
              <div className="wave-metric-label">Select a buoy to view wave data</div>
            </div>
          </div>
    ) :  (
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

      {/* Chart Panel */}
      <div className="panel chart-panel">
        <div className="panel-header">
          <h2 className="panel-title">Wave Height Timeline</h2>
        </div>
        <div className="chart-container">
          {!selectedBuoy ? (
            <div className="loading">Select a buoy to view wave data chart</div>
          ) : error ? (
            <div className="error">Error: {error}</div>
          ) : !data ? (
            <div className="loading">Loading chart data...</div>
          ) : (
            /* ResponsiveContainer makes the chart resize with the window */
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                {/* CartesianGrid adds the background grid lines */}
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
                {/* XAxis shows the time labels at bottom */}
                <XAxis 
                  dataKey="time" 
                  stroke="#a0a0a0"
                  fontSize={12}
                />
                {/* YAxis shows the wave height values on left */}
                <YAxis 
                  stroke="#a0a0a0"
                  fontSize={12}
                />
                {/* Tooltip shows details when you hover over points */}
                <Tooltip 
                  contentStyle={{
                    backgroundColor: '#1a1a1a',
                    border: '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '8px',
                    color: '#ffffff'
                  }}
                />
                {/* Legend explains what the lines represent */}
                <Legend />
                {/* The actual line that shows wave height data */}
                <Line 
                  type="monotone"           // Smooth curved line
                  dataKey="waveHeight"     // Which data to plot (from chartData)
                  stroke="#00d4ff"         // Line color (your blue theme)
                  strokeWidth={2}          // Line thickness
                  name="Wave Height (m)"   // Label in legend and tooltip
                  dot={{ fill: '#00d4ff', strokeWidth: 2, r: 4 }}
                  activeDot={{ r: 6, fill: '#00d4ff' }}
                />
              </LineChart>
            </ResponsiveContainer>
          )}
        </div>
      </div>

      {/* Historical Data Panel */}
      <div className="panel historical-panel">
        <div className="panel-header">
          <h2 className="panel-title">Historical Wave Data</h2>
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
              ) :error ? (
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
    </div>
  );

  // Render different pages based on current page state
  const renderPage = () => {
    switch (currentPage) {
      case 'settings':
        return <SettingsPage />;
      case 'about':
        return <AboutPage />;
      case 'dashboard':
      default:
        return <DashboardPage />;
    }
  };

  //JSX -> html and JS making user interface
  //if error shows <div> with error message
  //if valid data, loops through timestamps and metrics displayed
  return (
    <div className="app">
      {/* Top Navigation */}
      <nav className="top-nav">
        <div className="nav-container">
          <div className="logo" onClick={() => handleNavigation('dashboard')}>
            Surf Analytics Dashboard
          </div>
          
          {/* New Navigation Menu */}
          <div className="nav-menu">
            <button 
              className={`nav-button ${currentPage === 'dashboard' ? 'active' : ''}`}
              onClick={() => handleNavigation('dashboard')}
            >
              Dashboard
            </button>
            <button 
              className={`nav-button ${currentPage === 'settings' ? 'active' : ''}`}
              onClick={() => handleNavigation('settings')}
            >
              Settings
            </button>
            <button 
              className={`nav-button ${currentPage === 'about' ? 'active' : ''}`}
              onClick={() => handleNavigation('about')}
            >
              About
            </button>
          </div>
          
          <div className="nav-controls">
            <select
              className="nav-select"
              /*dropdown controlled by react*/
              value={selectedBuoy}
              /*function runs on user select*/
              onChange={handleBuoyChange}
            >
              <option value="">Select Buoy</option>
              {/*creates <option> element for each buoy in array*/}
              {buoyOptions.map((buoy) => (
                /*unique keys for list items*/
                <option key={buoy.id} value={buoy.id}>
                  {buoy.name} - {buoy.location}
                </option>
              ))}
            </select>
            <select
              className="nav-select"
              value={selectedWebcam}
              onChange={handleWebcamChange}
            >
              <option value="">Select Live Surfcam</option>
              {webcamOptions.map((webcam) => (
                <option key={webcam.id} value={webcam.id}>
                  {webcam.name} - {webcam.location}
                </option>
              ))}
            </select>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      {renderPage()}
    </div>
  );
}

export default App;
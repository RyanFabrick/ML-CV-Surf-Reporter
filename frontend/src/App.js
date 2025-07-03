//useState -> store and track data
//useEffect -> runs logic after component loads
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer} from 'recharts';
import './App.css';

//uses react state to track data and error
function App() {
  //data -> data from Flask backend
  const [data, setData] = useState(null);
  //error -> possible error during fetch
  const [error, setError] = useState(null);
  //add state for selected buoy
  const [selectedBuoy, setSelectedBuoy] = useState('273');
  //webcam specific state
  const [selectedWebcam, setSelectedWebcam]= useState('');
  const [videoData, setVideoData] = useState(null);
  const [webcamError, setWebcamError] = useState(null);
  const [analysisStatus, setAnalysisStatus] = useState('')
  
  //currently mock buoy data - (tentative update)
  const buoyOptions = [
    { id: '273', name: 'Point Dume, CA', location: 'Malibu' },
    { id: '191', name: 'Santa Monica Bay, CA', location: 'Santa Monica' },
    { id: '215', name: 'Harvest, CA', location: 'Point Arguello' },
    { id: '067', name: 'San Francisco Bar, CA', location: 'San Francisco' }
  ];

  //webcam options (tentative update, currently malibu only)
  const webcamOptions = [{
      id: 'malibu', 
      name: 'Malibu - Point Dume', 
      location: 'Malibu, CA',
      status: 'online',
      buoy_nearby: '273'
  }];

  //function handles buoy selection changes
  const handleBuoyChange = (event) => {
    const newBuoyId = event.target.value;
    setSelectedBuoy(newBuoyId);
    console.log(`Selected Buoy: ${newBuoyId}`);
  };

  // handles ebcam selection changes
  const handleWebcamChange = (event) => {
    const newWebcamId = event.target.value;

    //Stops previous analusis if switching webcams
    if (selectedWebcam && selectedWebcam !== newWebcamId) {
      fetch(`http://localhost:5000/api/stop-analysis/${selectedWebcam}`)
        .catch(err => console.log('Error Stopping Previous Analysos:', err));
    }


    setSelectedWebcam(newWebcamId);
    setVideoData(null);
    setWebcamError(null);
    setAnalysisStatus('')
    //data refreshues due to useEffect depednecny
    console.log(`Selected Webcam: ${newWebcamId || 'None'}`);
  };

  //runs after empty array is ran, after component mounts
  //fetches data from Flask endpoint
  //dtores in data, if error stores error message
  const fetchWaveData = (buoyId) => {
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
      //no webcam selected , clear data
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
          if (json.status === 'stating') {
            setAnalysisStatus('Stating Analysis...');
          } else if (json.status === 'initializing') {
            setAnalysisStatus('Initializing Analysis...');
          } else if (json.status === 'online') {
            setAnalysisStatus('Live'); 
          } else if (json.status ==='error') {
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
    //intial data fetch
    fetchWaveData(selectedBuoy);
    fetchVideoData(selectedWebcam);

    const waveInterval = setInterval(() => {
      fetchWaveData(selectedBuoy);
    } , 180000); //3 minutes

    const videoInterval = setInterval(() => {
      if (selectedWebcam) {
        fetchVideoData(selectedWebcam);
      }
    }, 5000); //5 seconds
    
    return () => {
      clearInterval(waveInterval);
      clearInterval(videoInterval);
    };

  }, [selectedBuoy, selectedWebcam]); //rerun when selection changes

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

const getStatusColor = (status) => {
  switch (status) {
    case 'online': return '#28a745';
    case 'starting': 
    case 'initializing': return '#ffc107';
    case 'error': return '#dc3545';
    default: return '#6c757d';
  }
};

//JSK -> html and JS making user interface
//if error shows <div> with error message
//if valid data, loops throgh timestamps and metrics dispalyed
  return (
    <div className="dashboard">
      <div className="title-box">
        <div className="title">Surf Forecast Data</div>
      </div>

      <div className="selection-container">
        <div className="selector-box">
          <label htmlFor="buoy-select" className="selector-label">
            Select Buoy Location:
          </label>
          <select
            id="buoy-select"
            /*dropdown controlled by react*/
            value={selectedBuoy}
            /*function runs on user select*/
            onChange={handleBuoyChange}
            className="location-dropdown"
            >
              {/*creates <option> element for each buoy in array*/}
              {buoyOptions.map((buoy) => (
                /*unique keys for list items*/
                <option key={buoy.id} value={buoy.id}>
                  {buoy.name} - {buoy.location}
                </option>
              ))}
            </select>
            <div className="selected-info">
              {/*gives optional chaining, access name even if buoy not found*/}
              Currently Showing: {buoyOptions.find(b => b.id === selectedBuoy)?.name}
            </div>
        </div>
        
        <div className="selector-box">
          <label htmlFor="webcam-select" className="selector-label">
            Select Live Webcam (CV/ML Analysis):
          </label>
          <select
            id="webcam-select"
            value={selectedWebcam}
            onChange={handleWebcamChange}
            className="location-dropdown"
            >
              <option value="">No Webcam - Buoy Data Only</option>
              {webcamOptions.map((webcam) => (
                <option key ={webcam.id} value={webcam.id}>
                  {webcam.name} - {webcam.location}
                  </option>
              ))}
            </select>
            <div className="selected-info">
              {selectedWebcam
                ? `CV/ML Analysis: ${webcamOptions.find(w => w.id === selectedWebcam)?.name}`
                : 'Visual Analysis Unavailable'}
            </div>
            {analysisStatus && (
              <div className={`analysis-status ${videoData?.status || 'default'}`}>
                Status: {analysisStatus}
              </div>
            )}
        </div>
      </div>

      {data && (
        <div className="chart-container">
          <h2 className="wave-chart-title">
            Wave Height Over Time - {buoyOptions.find(b => b.id === selectedBuoy)?.name}
            </h2>
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
      
      {/*video analysis - conditional show*/}
      {selectedWebcam && (
        <div className="video-analysis-container">
          {webcamError && (
            <div className="webcam-error">
              <h3>Webcam Data Unavailable</h3>
              <p>{webcamError}</p>
            </div>
          )}

          {videoData && !webcamError && (
            <>
              <h2 className="analysis-title">
                Live Visual Conditions - {videoData.location_name}
              </h2>
              {videoData.status === 'Starting' || videoData.status === 'Initializing' ? (
                <div className='analysis-loading'>
                  <h3>Setting up CV/ML Analysis...</h3>
                  <p>This may take 30-60 seconds as we:</p>
                  <ul className='loading-steps'>
                    <li>Connect to the live surf cam stream</li>
                    <li>Initalize ML Computer Vision model</li>
                    <li>Begin real-time surfer detection</li>
                  </ul>
                  <p className='loading-note'>Please Wait. The analysis will start automatically!</p>
                </div>
              ) : (
                <div className='analysis-grid'>
                  <div className='analysis-card surfer-card'>
                    <div className='card-content'>
                      <div className='card-number'>{videoData.surfer_count}</div>
                      <div className='card-label'>Surfers Out</div>
                    </div>
                  </div>

                  <div className='analysis-card status-card'>
                    <div className='card-content'>
                      <div className={`card-number status-indicator ${videoData.status}`}>
                        {videoData.status === 'online' ? '🟢' : '🔴'}
                      </div>
                      <div className='card-label'>Stream Status</div>
                    </div>
                  </div>
                </div>
              )}

              {videoData.last_update && (
                <div className='last-update'>
                Last Updated: {new Date(videoData.last_update).toLocaleString()}
                </div>
              )}
            </>
          )}
          </div>
      )}

      {/* Metrics Box - displays detailed wave measurements */}
      <div className="metrics-box">
        <h3>Detailed Wave Measurements</h3>
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
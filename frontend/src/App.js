//useState -> store and track data
//useEffect -> runs logic after component loads
import React, { useState, useEffect } from 'react';
import './App.css';

// Import components
import DashboardPage from './components/Dashboard_Page';
import SettingsPage from './components/Settings_Page';
import AboutPage from './components/About_Page';

// Import constants
import { buoyOptions } from './constants/Buoy_Options';
import { webcamOptions } from './constants/Webcam_Options';

// Import custom hooks
import { useWaveData } from './hooks/useWaveData';
import { useVideoData } from './hooks/useVideoData';

//uses react state to track data and error
function App() {
  //add state for selected buoy
  const [selectedBuoy, setSelectedBuoy] = useState('');
  //webcam specific state
  const [selectedWebcam, setSelectedWebcam] = useState('');
  //state for navigation
  const [currentPage, setCurrentPage] = useState('dashboard');
  //settings state - initialize with saved values or defaults
  const [theme, setTheme] = useState(() => {
    const savedTheme = localStorage.getItem('surf-analytics-theme');
    return savedTheme || 'dark';
  });
  const [fontSize, setFontSize] = useState(() => {
    const savedFontSize = localStorage.getItem('surf-analytics-font-size');
    return savedFontSize ? parseInt(savedFontSize) : 100;
  });

  //applies theme and font size throughout application
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    document.documentElement.style.fontSize = `${fontSize}%`;
  }, [theme, fontSize]); // Only run when theme or fontSize changes

  //save theme to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('surf-analytics-theme', theme);
  }, [theme]);

  //save font size to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('surf-analytics-font-size', fontSize.toString());
  }, [fontSize]);

  // Use custom hooks for data fetching
  const { data, error, fetchWaveData } = useWaveData(selectedBuoy);
  const { videoData, webcamError, analysisStatus, fetchVideoData } = useVideoData(selectedWebcam);
  
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
    //data refreshes due to useEffect dependency
    console.log(`Selected Webcam: ${newWebcamId || 'None'}`);
  };

  //theme change handler
  const handleThemeChange = (newTheme) => {
    setTheme(newTheme);
  };

  //font size change handler
  const handleFontSizeChange = (newFontSize) => {
    setFontSize(newFontSize);
  };

  // Render different pages based on current page state
  const renderPage = () => {
    switch (currentPage) {
      case 'settings':
        return (
        <SettingsPage
        onNavigate={handleNavigation}
        theme={theme}
        onThemeChange={handleThemeChange}
        fontSize={fontSize}
        onFontSizeChange={handleFontSizeChange}
        />
        ); 
      case 'about':
        return <AboutPage onNavigate={handleNavigation} />;
      case 'dashboard':
      default:
        return (
          <DashboardPage
            selectedBuoy={selectedBuoy}
            selectedWebcam={selectedWebcam}
            data={data}
            error={error}
            videoData={videoData}
            webcamError={webcamError}
            analysisStatus={analysisStatus}
            onNavigate={handleNavigation}
          />
        );
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
            Surf Reporter
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

      {renderPage()}
    </div>
  );
}

export default App;
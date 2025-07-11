# Surf Reporter Frontend

A modern, sleek, responsive React application that provides users with real-time surf and wave conditions as well as real-time surfer detection through live surf cameras.
## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [UI Preview](#ui-preview)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [API Integration](#api-integration)
- [Theme & Customization](#theme--customization)
- [Components Architecture](#components-architecture)
- [Custom Hooks](#custom-hooks)
- [Browser Support](#browser-support)
- [Security Considerations](#security-considerations)
- [Performance Optimizations](#performance-optimizations)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

## Overview

Surf Reporter's frontend is a cleanly designed web application that combines real-time oceanographic buoy data with computer vision technology to deliver comprehensive and live surf conditions for users. Built with React and featuring a smooth, customizable interface, it provides users with both quantitative wave data and live visual analysis of the number of surfers on live surf cameras.

## Features

### Real-Time Wave Data
- **Live Buoy Integration**: Real-time data from CDIP (Coastal Data Information Program) buoys
- **Comprehensive Metrics**: Wave height, peak period, direction, average period, zero-crossing period, and peak PSD (Power Spectral Density)
- **Interactive Chart**: Dynamic wave height timelines with Recharts visualization
- **Historical/Recent Data**: Tabular view of recent wave conditions with detailed timestamps

### Real-Time Surfer Detection
- **Computer Vision Integration**: Real-time surfer detection using a custom-trained machine learning model through Roboflow
- **Live Stream Processing**: Integration with live surf camera feeds via HLS (HTTP Live Streaming) to MJPEG (Motion JPEG) conversion
- **Surfer Count Display**: Live count of surfers in the water at user selected surf cameras
- **Stream Status Monitoring**: Real-time connection and analysis status indicators

## UI Preview

**Dashboard**

<p float="left">
  <figure>
    <img src="./public/videos/dashboard_darkmode_gif.gif" width="49%" />
    <figcaption align="center">Dark Mode</figcaption>
  </figure>
  <figure>
    <img src="./public/videos/dashboard_lightmode_gif.gif" width="49%" />
    <figcaption align="center">Light Mode</figcaption>
  </figure>
</p>

### User Experience
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Accessibility**: Scalable font sizes (80% - 150%) for improved readability
- **Dark/Light Mode**: Toggle between theme preferences with persistent storage
- **Intuitive Navigation**: Clean, modern interface with contextual help system

### Data Visualization
- **Interactive Chart**: Responsive, readable wave height timelines
- **Real-Time Updates**: Automatic data refresh intervals (3 minutes for wave data, 5 seconds for surf camera analysis)
- **Contextual Tooltips**: Detailed explanations of oceanographic terminology and computer vision and machine learning model
- **Export-Ready**: Clean data presentation suitable for analysis

## Technology Stack

### Core
- **React**: Modern hooks-based architecture with functional components
- **JavaScript**: Modern JavaScript features and best practices
- **CSS**: Custom properties for theming, responsive grid and flexbox layouts, backdrop filter effects, smooth transitions/animations, and dual theme support (dark/light mode)
- **HTML**: Semantic markup with accessibility considerations

### Libraries & Tools
- **Recharts**: Professional charting library for data visualization
- **React Hooks**: useState, useEffect for state management and lifecycle methods
- **Custom Hooks**: Reusable logic for data fetching and state management
- **LocalStorage API**: Persistent user preferences and settings

### Architecture Patterns
- **Component-Based Architecture**: Modular, reusable React components
- **Custom Hook Pattern**: Separated business logic from UI components
- **Service Layer**: Centralized API communication and data processing
- **Responsive Design**: Mobile-first approach using flexible layouts

## Project Structure

```
frontend/
├── node_modules/
├── public/
│   ├── videos/
│   ├── favicon.ico
│   ├── index.html
│   ├── logo192.png
│   ├── logo512.png
│   ├── manifest.json
│   └── robots.txt
├── src/
│   ├── components/
│   │   ├── About_Page.js
│   │   ├── Chart_Panel.js
│   │   ├── Dashboard_Page.js
│   │   ├── Historical_Data_Panel.js
│   │   ├── Settings_Page.js
│   │   ├── Video_Panel.js
│   │   └── Wave_Data_Panel.js
│   ├── constants/
│   │   ├── Buoy_Options.js
│   │   └── Webcam_Options.js
│   ├── hooks/
│   │   ├── useVideoData.js
│   │   └── useWaveData.js
│   ├── utils/
│   │   ├── getCurrentWaveData.js
│   │   └── prepareChartData.js
│   ├── App.css
│   ├── App.js
│   ├── App.test.js
│   ├── index.css
│   └── index.js
├── logo.svg
├── reportWebVitals.js
├── setupTests.js
├── .gitignore
├── package.json
├── package-lock.json
├── postcss.config.js
└── README.md
```

## Quick Start

### Prerequisites
- Node.js (v16 or higher)
- npm package manager
- Backend API server running on localhost:5000

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RyanFabrick/ML-CV-Surf-Reporter.git
   cd ML-CV-Surf-Forecast/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

4. **Open browser and navigate to**
   ```
   http://localhost:3000
   ```

### Available Scripts
- `npm start` - starts development server
- `npm run build` - builds the app for production
- `npm test` - launches the test runner
- `npm run eject` - ejects from Create React App (irreversible)

## API Integration

The frontend communicates with a Flask backend through RESTful APIs.

### Wave Data Endpoint
```javascript
fetch(`http://localhost:5000/api/surfdata?buoy_id=${buoyId}`)
```
- Fetches real-time wave conditions from CDIP buoys
- Updates every three minutes
- Returns comprehensive oceanographic data

### Video Analysis Endpoint
```javascript
fetch(`http://localhost:5000/api/video-analysis?webcam_id=${webcamId}`)
```
- Fetches live surfer detection results
- Updates every five seconds
- Provides stream status and surfer count

### Stop Analysis Endpoint
```javascript
fetch(`http://localhost:5000/api/stop-analysis/${selectedWebcam}`)
```
- Stops video analysis when switching surf cameras

### Error Handling Pattern
```javascript
.then((json) => {
  if (json.error) {
    setError(`Buoy Data Error: ${json.error}`);
  } else {
    setData(json);
  }
})
.catch((err) => {
  setError('Failed to fetch wave data - check connection');
});
```

### Data Processing
- **Time Parsing**: Converts API timestamps to readable formats
- **Data Validation**: Handles missing and/or invalid data gracefully
- **Performance Optimization**: Efficient data transformation and rendering

## Theme & Customization

### Theme System
- **CSS Custom Properties**: Dynamic theming with CSS variables
- **Dark Mode**: Professional dark theme with high contrast
- **Light Mode**: Bright, clean interface for daylight use
- **Persistent Storage**: Theme preferences saved in localStorage

### Typography
- **Scalable Fonts**: 80% to 150% size adjustment range
- **Accessible Design**: High contrast ratios and readable fonts and font sizes
- **Responsive Text**: Fluid typography that adapts to varying screen sizes

## Components Architecture

The application follows a component-based architecture with clear separation of concerns. Each component handles specific UI functionality and data presentation.

### Core Components

#### **Dashboard_Page.js**
- Main application dashboard that orchestrates all panels
- Receives and distributes props to child components
- Handles the overall layout and component composition
- Manages data flow between different sections

#### **Video_Panel.js**
- Displays live surfer detection results and current stream status
- Shows real-time surfer count and stream connectivity
- Provides loading states for computer vision machine learning model initialization
- Includes contextual help linking to computer vision explanations

#### **Wave_Data_Panel.js**
- Presents current wave conditions in a clean metric display
- Shows wave height, peak period, direction, and average period
- Handles loading states when no buoy is selected
- Formats numerical data with appropriate and readable units

#### **Chart_Panel.js**
- Renders interactive wave height timeline using Recharts
- Processes raw API data into chart-friendly format
- Provides responsive charting with hover tooltips
- Handles error states and loading indicators

#### **Historical_Data_Panel.js**
- Displays tabular view of recent wave data
- Shows comprehensive oceanographic metrics with timestamps
- Includes contextual help icon linking to metric explanations
- Handles data formatting and missing value display

#### **Settings_Page.js**
- Manages application customization options
- Provides theme switching (dark/light mode)
- Offers font size adjustment with live preview
- Handles user preference persistence

#### **About_Page.js**
- Comprehensive information about the application
- Explains computer vision pipeline and machine learning model details
- Details about stream processing and overall pipeline architecture
- Provides data source credits and external links
- Includes embedded video demonstration of computer vision model

### Component Communication

Components communicate through a combination of:
- **Props drilling**: Parent components pass data and callbacks down
- **Event callbacks**: Child components trigger parent actions via `onNavigate`
- **Shared state**: Global application state managed in the main App component
- **Context help**: Cross-component navigation with scroll-to-section functionality

## Custom Hooks

### useWaveData
```javascript
const { data, error, fetchWaveData } = useWaveData(selectedBuoy);
```
- Manages wave data fetching and state

### useVideoData
```javascript
const { videoData, webcamError, analysisStatus, fetchVideoData } = useVideoData(selectedWebcam);
```
- Handles video analysis data and real-time updates

## Browser Support

### Confirmed Browser Support
- Chrome
- Firefox
- Safari
- Edge

### Mobile Responsiveness
- **Responsive Grid Layout**: CSS Grid and Flexbox
- **Touch-Friendly Interface**: Optimized for mobile interaction
- **Adaptive Components**: Components scale appropriately across devices
- **Performance Optimized**: Efficient rendering on mobile devices

## Security Considerations

- **API Security**: Secure communication with backend services
- **Data Validation**: Client-side validation and sanitization
- **Error Handling**: Graceful error states and user feedback
- **CORS Configuration**: Proper cross-origin resource sharing setup

## Performance Optimizations

- **React.memo**: Prevents unnecessary re-renders
- **Custom Hooks**: Efficient data fetching and state management
- **Lazy Loading**: Components load as needed
- **Optimized Bundling**: Efficient code splitting and asset optimization

## Contributing

This project was developed as a personal learning project. For future questions and/or suggestions:

1. Open an issue describing the enhancement or bug
2. Fork the repository and create a feature branch
3. Submit a pull request with detailed description of changes

## License

This project is open source and available under the MIT License.

## Author

**Ryan Fabrick**
- Statistics and Data Science (B.S) Student, University of California Santa Barbara
- GitHub: [https://github.com/RyanFabrick](https://github.com/RyanFabrick)
- LinkedIn: [www.linkedin.com/in/ryan-fabrick](https://www.linkedin.com/in/ryan-fabrick)
- Email: ryanfabrick@gmail.com

## Acknowledgments

- **CDIP** (Coastal Data Information Program) - Buoy data source
- **The Surfers View** - Live surf camera feeds
- **Roboflow** - Computer vision and machine learning model training platform
- **FFmpeg** - Video stream processing and frame extraction
- **React Community** - Super helpful and clear documentation

________________________________________
Built with ❤️ for the surfing community
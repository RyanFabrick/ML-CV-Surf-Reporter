# *Surf Reporter* 

A comprehensive real-time surf monitoring application that combines computer vision, machine learning, and oceanographic data to provide live surf conditions and automated surfer detection.

## Table of Contents
- [Frontend, Backend, & Scripts READMEs (way more detail)](#frontend-backend--scripts-readmes-way-more-detail--demo-gifs)
- [Overview](#overview)
- [Why Did I Build This?](#why-did-i-build-this)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Demo GIFs](#demo-gifs)
- [Custom Trained Computer Vision & Machine Learning Model in Action](#custom-trained-computer-vision--machine-learning-model-in-action)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Computer Vision & Machine Learning Model Performance](#computer-vision--machine-learning-model-performance)
- [API Documentation](#api-documentation)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Acknowledgments & References](#acknowledgments--references)

## Frontend, Backend & Scripts READMEs (Way More Detail & Demo GIFs)

For more **comprehensive**, **specific**, and **thorough** documentation on Frontend, Backend, and Scripts:
- [Frontend README](frontend/README.md)
- [Backend README](backend/README.md)
- [Scripts README](scripts/README.md)

## Overview

*Surf Reporter* is a full-stack web application designed to enhance surf monitoring through real-time buoy data metrics combined with computer vision and machine learning. The system processes HLS (HTTP Live Streaming) video from surf cameras worldwide, detects surfers using a custom-trained machine learning model, and integrates real-time wave data from CDIP (Coastal Data Information Program) buoys to provide comprehensive surf and wave conditions for users.

## Why Did I Build This?

I built this personal project to grow my skills and knowledge in computer science and data science through something that feels close to home. As a UCSB student living in Isla Vista, California, surfing isn’t just a hobby; it’s woven into the community and daily life around me.

I’ve always noticed how popular companies like *Surfline* use live surf cameras and data to help surfers, but most of their features are hidden behind steep paywalls. I wanted to do something different: build my own application that taps into live surf cameras, leverages computer vision and machine learning, and keeps everything completely free and open for anyone to use.

This project became a way to blend what I’m passionate about, technology and surfing, into something real, useful, and shareable.

### Key Capabilities
- Real-time surfer detection using custom computer vision models via Roboflow
- Live oceanographic buoy data from CDIP buoy network
- Multi-stream, concurrent video processing with automatic health monitoring
- Responsive web interface
- Professional-grade data visualization and analytics

## Features

### Computer Vision & Machine Learning
- **Custom-Trained Model**: Purpose-built surfer detection algorithm with 65.4% mAP@50, 69.3% precision, 63.9% recall
- **Real-Time Processing**: Live inference and optimized frame processing on multiple live video streams simultaneously
- **Roboflow Integration**: Cloud-based machine learning pipeline for scalable object detection and classification
- **Automated Health Monitoring**: Automatic stream processing with error handling, recovery, and logging

### Oceanographic Data Integration
- **Live Buoy Data**: Real-time wave conditions from CDIP THREDDS servers accessed via OPenDAP
- **Comprehensive Data Metrics**: Wave height, peak period, direction, average period, zero-crossing period, and peak PSD (Power Spectral Density)
- **Data Quality Validation**: Automatic filtering of invalid, corrupted, and weak data points
- **Historical Data Analysis**: Time series data processing and trend analysis on varying data metrics

### Modern Web User Interface
- **Responsive Design**: Optimized for desktop, tablet, and mobile devices
- **Accessibility Features**: Scalable fonts (80%-150%), high contrast ratios, and dark/light theme
- **Real-Time Updates**: Live data refresh with configurable intervals
- **Interactive Visualizations**: Professional charts and data presentations

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        React Frontend                           │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                 │
│ │ Dashboard   │ │ Settings    │ │ About       │                 │
│ │ Page        │ │ Page        │ │ Page        │                 │
│ └─────────────┘ └─────────────┘ └─────────────┘                 │
│                                                                 │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                 │
│ │Video Panel  │ │Wave Data    │ │Chart Panel  │                 │
│ │             │ │Panel        │ │             │                 │
│ └─────────────┘ └─────────────┘ └─────────────┘                 │ 
└─────────────────────────┼───────────────────────────────────────┘
                          │ RESTful API
┌─────────────────────────┼───────────────────────────────────────┐
│                    Flask Backend                                │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                 │
│ │Video        │ │Surf Data    │ │Frontend     │                 │
│ │Analysis     │ │Routes       │ │Routes       │                 │
│ └─────────────┘ └─────────────┘ └─────────────┘                 │
│                                                                 │
│ ┌─────────────┐ ┌─────────────┐                                 │
│ │LiveStream   │ │CDIP THREDDS │                                 │
│ │Analyzer     │ │Integration  │                                 │
│ └─────────────┘ └─────────────┘                                 │
└─────────────────────────┼───────────────────────────────────────┘
                          │
┌─────────────────────────┼───────────────────────────────────────┐
│                  External Services                              │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                 │
│ │HLS Streams  │ │Roboflow API │ │CDIP Buoys   │                 │
│ │(Surf Cams)  │ │(ML Model)   │ │(Wave Data)  │                 │
│ └─────────────┘ └─────────────┘ └─────────────┘                 │
└─────────────────────────────────────────────────────────────────┘
```

## Demo GIFs

**Dashboard**

![demo gif 1 dark](https://github.com/user-attachments/assets/8f4d11f3-323a-4dbc-b821-fbe4ddff2b8a)

![demo 3 gif light](https://github.com/user-attachments/assets/6b5b7878-568f-4d85-b0f5-0a5056d509cc)

**Settings Page & About Page**

![demo gif 2 dark](https://github.com/user-attachments/assets/70de193e-cd4c-4537-856e-96ea1d1e8d67)

![demo 4 gif light](https://github.com/user-attachments/assets/b10611fe-fa83-4ea7-8934-17f4d0146403)

## Custom Trained Computer Vision & Machine Learning Model in Action

![example_video_gif](https://github.com/user-attachments/assets/a55c25ad-a6e1-444e-adf3-b057ca1109dc)

## Technology Stack

### Frontend
- **React**: Modern hooks-based architecture with functional components
- **JavaScript**: ES6+ features and best practices
- **CSS**: Custom properties, responsive and flexible layouts, dual theme support
- **Recharts**: Professional data visualization library
- **Custom Hooks**: Reusable logic for data fetching and state management

### Backend
- **Python**: Primary programming language
- **Flask**: Lightweight web framework optimized for API services
- **FFmpeg**: Professional video stream processing, conversion, and frame extraction
- **OpenCV**: Computer vision library for image processing and analysis
- **ML & CV Inference**: Real-time object detection via Roboflow InferencePipeline
- **Threading**: Concurrent processing for multiple streams

### Machine Learning & Computer Vision
- **Roboflow**: Cloud-based object detection and classification platform
- **Custom Computer Vision Pipeline**: Purpose-built, custom surfer detection algorithm
- **Real-time Inference**: Live model inference on live video streams
- **Performance Optimized**: Efficient frame processing and analysis

### Data Processing
- **xarray**: Multi-dimensional array processing for NetCDF data
- **pandas**: Data manipulation and time series analysis
- **NumPy**: Numerical computing and array operations
- **OPeNDAP**: Direct integration for CDIP THREDDS data server

## Project Structure

```
backend/
├── analysis/
│   ├── live_stream_analyzer.py
│   └── roboflow_utils.py
├── routes/
│   ├── frontend.py
│   ├── surf_data.py
│   └── video_analysis.py
├── .env
├── .gitignore
├── app.py
├── backend_tests.py
├── config.py
├── requirements.txt
└── webcam_configs.py

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

scripts/
├── CV_pipeline_TEST.py
├── CV_pipeline_TEST2.py
├── frame_extraction.py
└── README.md
```

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- FFmpeg installed and accessible in PATH
- Roboflow API key and workspace access
- Sufficient hardware for concurrent stream processing

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RyanFabrick/ML-CV-Surf-Forecast.git
   cd ML-CV-Surf-Forecast
   ```

2. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
   # Configure environment variables
   cp .env.example .env
   # Edit .env with your Roboflow credentials
   ```

3. **Frontend Setup**
   ```bash
   cd ../frontend
   npm install
   ```

4. **Start the Application**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python app.py
   
   # Terminal 2 - Frontend
   cd frontend
   npm start
   ```

5. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

## Configuration

### Environment Variables

The application requires several environment variables to be configured for proper operation. These variables handle external service integration, API authentication, and system behavior.

### Backend Configuration

Create a `.env` file in the `backend/` directory with the following variables:

```env
# Roboflow API Configuration
ROBOFLOW_API_KEY=your_roboflow_api_key_here
ROBOFLOW_WORKSPACE=your_workspace_name
ROBOFLOW_WORKFLOW_ID=your_workflow_id

# Flask Application Settings
FLASK_ENV=development
FLASK_DEBUG=True
API_PORT=5000

# Stream Processing Configuration
FFMPEG_TIMEOUT=30
MAX_CONCURRENT_STREAMS=5
FRAME_RATE=1
```

### Required Variables

**ROBOFLOW_API_KEY**
- **Purpose**: Authentication key for accessing Roboflow's machine learning inference services
- **Why needed**: Enables real-time surfer detection through the custom-trained computer vision model
- **How to obtain**: Sign up at Roboflow, create a workspace, and generate an API key from your account settings

**ROBOFLOW_WORKSPACE**
- **Purpose**: Identifies your specific Roboflow workspace containing the trained model
- **Why needed**: Directs API calls to the correct model deployment environment
- **Format**: Usually your username or organization name

**ROBOFLOW_WORKFLOW_ID**
- **Purpose**: Specifies the exact workflow/model version to use for inference
- **Why needed**: Ensures consistent model performance and version control
- **How to obtain**: Found in your Roboflow project dashboard under workflow settings

### Optional Configuration Variables

**FLASK_ENV**
- **Purpose**: Sets the Flask application environment mode
- **Default**: `development`
- **Options**: `development`, `production`, `testing`

**FLASK_DEBUG**
- **Purpose**: Enables/disables Flask debug mode for development
- **Default**: `True` for development
- **Production**: Set to `False` for production deployments

**API_PORT**
- **Purpose**: Specifies the port for the Flask backend server
- **Default**: `5000`
- **Note**: Ensure this port is available and not blocked by firewall

**FFMPEG_TIMEOUT**
- **Purpose**: Maximum time (seconds) to wait for FFmpeg stream processing
- **Default**: `30`
- **Why needed**: Prevents hanging processes when streams are unavailable

**MAX_CONCURRENT_STREAMS**
- **Purpose**: Limits the number of simultaneous video streams processed
- **Default**: `5`
- **Why needed**: Prevents resource exhaustion and maintains system stability

**FRAME_RATE**
- **Purpose**: Frames per second for video analysis processing
- **Default**: `1` (one frame per second)
- **Why needed**: Balances detection accuracy with computational efficiency

## Data Source Configuration

### CDIP Buoy Integration

The application automatically connects to CDIP (Coastal Data Information Program) THREDDS data server via OpenDAP protocol. No additional configuration is required for buoy data access.

**Supported Buoy Networks:**
- Real-time oceanographic data from 100+ CDIP buoys
- Automatic data quality validation and filtering
- Historical data access for trend analysis

### Surf Camera Stream URLs

Stream URLs are preconfigured in `backend/webcam_configs.py`. The application supports HLS (HTTP Live Streaming) sources from:

**Default Sources:**
- The Surfers View camera network

**Adding Custom Streams:**
```python
# In webcam_configs.py
WEBCAM_CONFIGS = {
    'custom_location': {
        'name': 'Custom Surf Spot',
        'url': 'https://your-hls-stream-url.com/playlist.m3u8',
        'location': 'Custom Location, State'
    }
}
```

## System Requirements

**Hardware Requirements:**
- **CPU**: Sufficient enough for multiple, concurrent stream processing
- **RAM**: Sufficient enough for multiple, concurrent stream processing
- **Storage**: Recommended 2GB free space for dependencies and temporary files
- **Network**: Stable broadband connection

**Software Dependencies:**
- **FFmpeg**: Required for video stream processing and format conversion
- **Python**: Version 3.8 or higher
- **Node.js**: Version 16 or higher for frontend development

## Verification

After configuration, verify your setup:

```bash
# Test backend configuration
cd backend
python -c "from config import Config; print('✓ Backend configuration loaded')"

# Test Roboflow API connection
python -c "from roboflow import Roboflow; rf = Roboflow(api_key='your_key'); print('✓ Roboflow connected')"

# Test FFmpeg installation
ffmpeg -version

# Start application
python app.py
```

## Security Considerations

- **Never commit `.env` files** to version control
- **Use environment-specific configurations** for development/production
- **Rotate API keys regularly** for security
- **Restrict API key permissions** to minimum required scope
- **Use HTTPS in production** for secure data transmission

## Troubleshooting Configuration

**Common Issues:**
- **Missing API Key**: Ensure ROBOFLOW_API_KEY is set and valid
- **Stream Connection Failures**: Verify internet connectivity and stream URLs
- **FFmpeg Errors**: Confirm FFmpeg is installed and accessible in PATH
- **Port Conflicts**: Ensure configured ports (5000, 3000) are available

## Computer Vision & Machine Learning Model Performance

My custom-trained computer vision model on Roboflow achieves the following metrics:
- **mAP@50**: 65.4%
- **Precision**: 69.3%
- **Recall**: 63.9%
- **Training Dataset**: 200+ annotated surf images
- **Real-time Processing**: Configurable FPS (frames per second) on live streams

## API Documentation

### Video Analysis
```http
GET /api/video-analysis?webcam_id=<webcam_id>
```
Returns real-time surfer detection results with confidence scores and stream status.

### Wave Data
```http
GET /api/surfdata?buoy_id=<buoy_id>
```
Fetches comprehensive oceanographic data from CDIP buoy networks.

### Live Video Feed
```http
GET /video_feed/<webcam_id>
```
Streams processed video feed with ML overlay (MJPEG format).

## Testing

### Backend Tests
```bash
cd backend
python -m pytest tests/ -v --cov=. --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Docker Deployment
```bash
# Backend
cd backend
docker build -t surf-reporter-backend .
docker run -p 5000:5000 surf-reporter-backend

# Frontend
cd frontend
docker build -t surf-reporter-frontend .
docker run -p 3000:3000 surf-reporter-frontend
```

### Production Considerations
- Load balancing for multiple backend instances
- SSL/TLS configuration
- Resource monitoring and scaling
- Health check endpoints
- Automated backup and recovery

## Contributing

This project was developed as a personal learning project. For future questions and/or suggestions:

1. Open an issue describing the enhancement or bug
2. Fork the repository and create a feature branch
3. Follow coding standards
4. Write tests for new functionality
5. Update documentation as needed
6. Submit a pull request with detailed description of changes

## License

This project is open source and available under the MIT License.

## Author

**Ryan Fabrick**
- Statistics and Data Science (B.S) Student, University of California Santa Barbara
- GitHub: [https://github.com/RyanFabrick](https://github.com/RyanFabrick)
- LinkedIn: [www.linkedin.com/in/ryan-fabrick](https://www.linkedin.com/in/ryan-fabrick)
- Email: ryanfabrick@gmail.com

## Acknowledgments & References

- **[CDIP (Coastal Data Information Program)](https://cdip.ucsd.edu/)** - Buoy oceanographic data source
- **[The Surfers View](https://www.thesurfersview.com/)** - Live surf camera feed provider
- **[Roboflow](https://roboflow.com/)** - Computer vision and machine learning model training infrastructure
- **[FFmpeg](https://ffmpeg.org/)** - Professional video stream processing and frame extraction capabilities
- **[Flask Community](https://flask.palletsprojects.com/)** - Excellent web framework
- **[React Community](https://react.dev/)** - Super helpful and clear documentation

________________________________________
Built with ❤️ for the surfing community

This personal project demonstrates my full-stack development skills, machine learning and computer vision integration, real-time data processing, and modern web technologies and development. I designed this as a portfolio piece showcasing my technical capabilities across multiple domains.

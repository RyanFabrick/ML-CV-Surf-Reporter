# *Surf Reporter* 

A comprehensive real-time surf monitoring application that combines computer vision, machine learning, and oceanographic data to provide live surf conditions and automated surfer detection.

## Documentation

For more **comprehensive**, **specific**, and **thorough** documentation on Frontend and Backend:
- [Frontend README](frontend/README.md)
- [Backend README](backend/README.md)

## Overview

*Surf Reporter* is a full-stack web application designed to enhance surf monitoring through real-time buoy data metrics combined with computer vision and machine learning. The system processes HLS (Live HTTP Streaming) video from surf cameras worldwide, detects surfers using a custom-trained machine learning model, and integrates real-time wave data from CDIP (Coastal Data Information Program) buoys to provide comprehensive surf and wave conditions for users.

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

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- FFmpeg installed and accessible in PATH
- Roboflow API key

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
- GitHub: https://github.com/RyanFabrick
- LinkedIn: www.linkedin.com/in/ryan-fabrick
- Email: ryanfabrick@gmail.com

## Acknowledgments

- **CDIP (Coastal Data Information Program)** - Oceanographic buoy data source
- **The Surfers View** - Live surf camera feeds
- **Roboflow** - Computer vision and machine learning model training platform
- **FFmpeg** - Video stream processing and frame extraction
- **React & Flask Communities** - Excellent documentation and super helpful support

________________________________________
Built with ❤️ for the surfing community

This personal project demonstrates my full-stack development skills, machine learning and computer vision integration, real-time data processing, and modern web technologies and development. I designed this as a portfolio piece showcasing my technical capabilities across multiple domains.
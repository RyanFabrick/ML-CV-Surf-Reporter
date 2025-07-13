# *Surf Reporter* Backend

A real-time computer vision system designed and trained for automated surfer detection. Surf and wave condition monitoring using live buoy oceanographic data.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Main Page Real-Time Surfer Detection](#real-time-surfer-detection-on-main-page)
- [System Architecture](#system-architecture)
- [Technology Stack](#technology-stack)
- [Computer Vision & Machine Learning Model in Action](#custom-trained-computer-vision--machine-learning-model-in-action)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Core Components](#core-components)
- [Testing & Quality Assurance](#testing--quality-assurance)
- [Security & Best Practices](#security--best-practices)
- [Performance Optimizations](#performance-optimizations)
- [Monitoring & Observability](#monitoring--observability)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Development Setup](#development-setup)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Acknowledgments](#acknowledgments)

## Overview

*Surf Reporter*'s backend is a robust Flask application that combines computer vision, real-time video processing, and live buoy oceanographic data analysis to provide comprehensive and up-to-date surf monitoring capabilities. This system processes HLS (HTTP Live Streaming) video streams from varying surf cameras worldwide, detects surfers using a custom-trained machine learning model, and aggregates wave data from CDIP (Coastal Data Information Program) buoys.

## Features

- **Real-time Surfer Detection**: Machine learning powered computer vision using Roboflow inference pipelines
- **Multi-stream Processing**: Concurrent analysis of multiple live surf camera feeds using threading
- **Live Video Streaming**: FFmpeg-based HLS to MJPEG (Motion JPEG) conversion for web compatibility
- **Oceanographic Data Integration**: Real-time wave data from CDIP buoy networks
- **Robust Error Handling**: Automatic recovery and health monitoring systems
- **RESTful API Design**: Clean, documented endpoints for frontend integration

## Real-Time Surfer Detection on Main Page
  ![backend gif](https://github.com/user-attachments/assets/f0e1f27c-a2ae-4054-8106-721ad505d40a)


## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Flask Backend                            │
├─────────────────────────────────────────────────────────────────┤
│ Routes:                                                         │
│ • /api/video-analysis • /api/surfdata • /                       │
└─────────────────────────────────────────────────────────────────┘
                                    │
            ┌───────────────────────┼───────────────────────┐
            │                       │                       │
            ▼                       ▼                       ▼
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│ Video Analysis  │       │   Surf Data     │       │   Frontend      │
│                 │       │                 │       │                 │
│ • Webcam Mgmt   │       │ • CDIP Buoys    │       │ • Static Files  │
│ • Stream Proxy  │       │ • Wave Data     │       │ • Templates     │
└─────────────────┘       └─────────────────┘       └─────────────────┘
         │                          │
         ▼                          ▼
┌─────────────────┐       ┌─────────────────┐
│LiveStreamAnalyzer│      │ CDIP THREDDS    │
│                 │       │                 │
│ ┌─────────────┐ │       │ • NetCDF Files  │
│ │FFmpeg Process│|       │ • Wave Heights  │
│ │HLS → MJPEG  │ │       │ • Periods       │
│ └─────────────┘ │       │ • Directions    │
│                 │       └─────────────────┘
│        ▼        │
│ ┌─────────────┐ │
│ │Roboflow API │ │
│ │ML Detection │ │
│ │Count Surfers│ │
│ └─────────────┘ │
└─────────────────┘
         │
         ▼
┌─────────────────┐
│ External APIs   │
│                 │
│ • HLS Streams   │
│ • Roboflow ML   │
│ • CDIP Buoys    │
└─────────────────┘
```

## Technology Stack

### Core
- **Python**: Primary programming language
- **Flask**: Lightweight web framework optimized for API services
- **FFmpeg**: Professional-grade video stream processing and conversion
- **OpenCV**: Computer vision library for image processing and analysis
- **Threading**: Concurrent processing architecture for multi-stream handling

### Machine Learning & Computer Vision
- **Roboflow Inference**: Cloud-based object detection and classification platform
- **Custom Computer Vision Pipeline**: Purpose-built, custom surfer detection algorithm
- **Real-time Processing**: Live inference and optimized frame processing
- **Model Performance**: 65.4% mAP@50, 69.3% precision, 63.9% recall on surfer detection

### Data Processing
- **xarray**: Multi-dimensional array processing for NetCDF buoy oceanographic data
- **pandas**: Data manipulation and time series analysis
- **NumPy**: Numerical computing and array operations
- **OpenDAP**: Direct Integration with CDIP THREDDS Data Server

### External APIs & Services
- **CDIP THREDDS Data Server**: Real-time oceanographic data via standardized protocols
- **Roboflow API**: Hosted machine learning model inference services
- **HLS Streaming**: Live video feed integration from surf cameras
- **The Surfers View**: Primary live surf camera feed provider

## Custom-Trained Computer Vision & Machine Learning Model in Action

![example_video_gif](https://github.com/user-attachments/assets/a794ac81-79de-446d-9246-89ff1fcffc51)

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
```

## Getting Started

### Prerequisites
- Python 3.8 or higher
- FFmpeg installed and accessible in PATH
- Roboflow API key and workspace access
- Sufficient hardware for concurrent stream processing

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/RyanFabrick/ML-CV-Surf-Forecast.git
   cd ML-CV-Surf-Forecast/backend
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install FFmpeg**
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   
   # Windows
   # Download from https://ffmpeg.org/download.html and add to PATH
   ```

### Configuration

1. **Create environment configuration**
   ```bash
   cp .env.example .env
   ```

2. **Configure environment variables**
   ```env
   # Roboflow Configuration
   ROBOFLOW_API_KEY=your_roboflow_api_key
   ROBOFLOW_WORKSPACE=your_workspace_name
   ROBOFLOW_WORKFLOW_ID=your_workflow_id
   
   # Application Configuration
   FLASK_ENV=development
   FLASK_DEBUG=True
   API_PORT=5000
   
   # Stream Processing Configuration
   FFMPEG_TIMEOUT=30
   MAX_CONCURRENT_STREAMS=5
   FRAME_RATE=1
   ```

3. **Verify configuration**
   ```bash
   python -c "from config import Config; print('✓ Configuration loaded successfully')"
   ```

### Running the Application

```bash
# Development mode
python app.py

# Production mode with Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 app:app
```

The API will be available at `http://localhost:5000`

## API Documentation

### Video Analysis Endpoints

#### Start Video Analysis
```http
GET /api/video-analysis?webcam_id=<webcam_id>
```

**Parameters:**
- `webcam_id` (string): Unique identifier for the webcam source

**Response:**
```json
{
  "webcam_id": "Windansea",
  "location_name": "Windansea - La Jolla",
  "surfer_count": 3,
  "status": "online",
  "confidence_scores": [0.85, 0.92, 0.78],
  "last_update": "2024-01-15T10:30:00Z",
  "model_version": "v1.2.0"
}
```

#### Stop Video Analysis
```http
GET /api/stop-analysis/<webcam_id>
```

**Response:**
```json
{
  "status": "stopped",
  "webcam_id": "Windansea",
  "message": "Analysis stopped successfully"
}
```

#### Live Video Feed
```http
GET /video_feed/<webcam_id>
```

**Response:** `multipart/x-mixed-replace` MJPEG stream

### Surf Data Endpoints

#### Get Wave Data
```http
GET /api/surfdata?buoy_id=<buoy_id>
```

**Parameters:**
- `buoy_id` (string): CDIP buoy identifier

**Response:**
```json
{
  "buoy_id": "100",
  "location": "Point Reyes, CA",
  "time": ["2024-01-15 10:00 AM", "2024-01-15 10:30 AM"],
  "waveHs": [1.2, 1.5],
  "waveTp": [8.5, 9.2],
  "waveDp": [225, 230],
  "waveTa": [6.8, 7.1],
  "waveTz": [5.9, 6.2],
  "wavePeakPSD": [0.8, 0.9],
  "data_quality": "excellent",
  "last_update": "2024-01-15T10:45:00Z"
}
```

### Error Handling

All endpoints return standardized error responses:
```json
{
  "error": "Detailed error message",
  "error_code": "STREAM_UNAVAILABLE",
  "timestamp": "2024-01-15T10:30:00Z",
  "request_id": "uuid-string"
}
```

## Core Components

### LiveStreamAnalyzer Class

The central component responsible for:
- **Stream Conversion**: HLS to MJPEG using optimized FFmpeg parameters
- **ML & CV Inference**: Real-time object detection via Roboflow InferencePipeline
- **Health Monitoring**: Automatic process recovery and error handling
- **Threading**: Concurrent processing for multiple streams

```python
class LiveStreamAnalyzer:
    def __init__(self, webcam_id, hls_url):
        self.webcam_id = webcam_id
        self.hls_url = hls_url
        self.inference_pipeline = None
        self.ffmpeg_process = None
    
    def start_analysis(self):
        """Initialize FFmpeg conversion and start ML inference"""
        
    def stop_analysis(self):
        """Clean shutdown of all processes"""
        
    def process_frame(self, frame):
        """Custom callback for ML inference results"""
```

### Video Processing Pipeline

1. **Input Ingestion**: HLS stream from live surf camera source
2. **Format Conversion**: FFmpeg processes HLS to MJPEG with standardized parameters
3. **Frame Extraction**: Individual frames extracted at configurable intervals
4. **ML & CV Inference**: Custom-trained roboflow model detects and classifies surfers
5. **Result Aggregation**: Surfer count and confidence scores compiled
6. **Output Delivery**: Real-time detection results via Flask API endpoints

### Data Processing Engine

#### CDIP Integration Features
- **OpenDAP Protocol**: Direct access to CDIP THREDDS data servers
- **Quality Validation**: Automatic filtering of invalid or corrupted data points
- **Time Series Processing**: Efficient handling of buoy oceanographic data
- **Format Standardization**: Consistent JSON output for frontend consumption

#### Performance Optimizations
- **Vectorized Operations**: NumPy-based array processing
- **Lazy Loading**: Data fetched only when requested
- **Parallel Processing**: Concurrent data fetching and processing

## Testing & Quality Assurance

### Test Coverage

The comprehensive test suite covers all major components:

```bash
# Run complete test suite
python -m pytest tests/ -v --cov=. --cov-report=html

# Run specific test categories
python -m pytest tests/test_video_analysis.py -v
python -m pytest tests/test_surf_data.py -v
python -m pytest tests/test_integration.py -v
```

### Test Categories
- **Unit Tests**: Individual component functionality
- **Integration Tests**: API endpoint validation and cross-component interaction
- **Performance Tests**: Load testing and resource utilization
- **Mock Testing**: External service simulation for reliable testing
- **Error Handling**: Comprehensive failure scenario coverage

### Code Quality Standards
- **Type Hints**: Comprehensive type annotation for better code clarity
- **Documentation**: Detailed docstrings for all public methods
- **Error Handling**: Graceful degradation and comprehensive logging

## Security & Best Practices

### Security Measures
- **Environment Variables**: Secure API key management with no hardcoded secrets
- **Input Validation**: Request parameter sanitization
- **CORS Configuration**: Secure cross-origin resource sharing setup
- **Error Handling**: Graceful future management
- **Error Sanitization**: Secure error messages without sensitive information disclosure

### Production Best Practices
- **Resource Management**: Proper cleanup of FFmpeg processes and file handles
- **Memory Management**: Efficient handling of video streams and large datasets
- **Process Monitoring**: Health checks and automatic restart processes
- **Logging**: Comprehensive application logging for debugging and monitoring
- **Configuration Management**: Environment-based configuration with validation

## Performance Optimizations

### Stream Processing Optimizations
- **Concurrent Processing**: Multi-threaded architecture for handling multiple streams
- **Resource Pooling**: Efficient FFmpeg process management and reuse
- **Frame Rate Optimization**: Configurable processing rates based on use case
- **Stream Optimization**: Configurable quality and frame rate settings

### Data Processing Optimizations
- **Vectorized Operations**: NumPy-based array processing for oceanographic data
- **Lazy Loading**: Data fetched only when required
- **Batch Processing**: Efficient bulk data operations

## Monitoring & Observability

### Application Monitoring
- **Health Checks**: Automated endpoint health monitoring
- **Performance Metrics**: Real-time performance tracking and alerting
- **Debug Information**: Detailed troubleshooting output
- **Error Tracking**: Comprehensive error logging and alerting

### Stream Processing Monitoring
- **Stream Health**: Real-time monitoring of video stream availability
- **Processing Latency**: Frame processing time tracking
- **Throughput Metrics**: Frames processed per second tracking

## Deployment

### Docker Deployment

```dockerfile
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "app:app"]
```

### Docker Compose

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "5000:5000"
    environment:
      - ROBOFLOW_API_KEY=${ROBOFLOW_API_KEY}
      - ROBOFLOW_WORKSPACE=${ROBOFLOW_WORKSPACE}
      - ROBOFLOW_WORKFLOW_ID=${ROBOFLOW_WORKFLOW_ID}
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - backend
    restart: unless-stopped
```

### Production Considerations
- **Load Balancing**: Multiple backend instance deployment
- **SSL/TLS**: HTTPS configuration with Let's Encrypt certificates
- **Resource Limits**: Memory, CPU, RAM constraints
- **Health Checks**: Health check configurations
- **Monitoring**: Application performance monitoring
- **Scaling**: Horizontal scaling capabilities

## Troubleshooting

### Common Issues

#### FFmpeg Configuration
```bash
# Verify FFmpeg installation
ffmpeg -version

# Check FFmpeg PATH configuration
which ffmpeg

# Test basic video processing
ffmpeg -f lavfi -i testsrc=duration=10:size=320x240:rate=1 test.mp4
```

#### Stream Connection Issues
- **Check Webcam URL Accessibility**: Verify HLS stream URLs are publicly accessible
- **Network Connectivity**: Ensure stable internet connection for stream processing
- **Port Availability**: Verify local ports (8550+) are available for MJPEG streams
- **Firewall Configuration**: Check firewall rules for outbound connections

#### Roboflow API Issues
- **API Key Validation**: Verify API key has proper permissions
- **Quota Limits**: Check inference quota and usage limits
- **Model Deployment**: Ensure model is properly deployed and accessible
- **Network Connectivity**: Verify connection to Roboflow inference servers

## Development Setup

```bash
# Clone forked repository
git clone https://github.com/yourusername/ML-CV-Surf-Forecast.git

# Create feature branch
git checkout -b feature/amazing-feature

# Install development dependencies
pip install -r requirements-dev.txt

# Run tests before committing
python -m pytest tests/ -v

# Commit changes
git commit -m 'Add amazing feature'

# Push to branch
git push origin feature/amazing-feature
```

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

- **CDIP (Coastal Data Information Program)** - Buoy oceanographic data source
- **The Surfers View** - Live surf camera feed provider
- **Roboflow** - Computer vision and machine learning model training infrastructure
- **FFmpeg** - Professional video stream processing and frame extraction capabilities
- **Flask Community** - Excellent web framework

________________________________________
Built with ❤️ for the surfing community

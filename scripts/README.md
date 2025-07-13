# *Surf Reporter* Scripts

Development and testing scripts I used during the creation of *Surf Reporter* person project application. These scripts were essential for prototyping, proof of concepts, testing computer vision pipelines, and developing the core functionality before integration into the main application. 

These scripts represent the foundational development work that made the production *Surf Reporter* application possible. These demonstrate the iterative process from concept to implementation, showcasing the evolution of computer vision and machine learning integration in a real-time application developed by me!

## Table of Contents
- [Overview](#overview)
- [Project Structure](#project-structure)
- [Development Pipeline](#development-pipeline)
- [Script Details](#script-details)
- [Usage Examples](#usage-examples)
- [Dependencies](#dependencies)
- [Integration with Main Application](#integration-with-main-application)
- [Development Workflow](#development-workflow)
- [Troubleshooting](#troubleshooting)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)
- [Acknowledgments & References](#acknowledgments--references)

## Overview

This folder contains the experimental and development scripts that were crucial in building the computer vision and machine learning capabilities of *Surf Reporter*. These scripts represent the iterative development process from proof-of-concept to production-ready implementation.

The scripts focus on:
- **Computer Vision Pipeline Development**: Testing HLS (HTTP Live Steaming) stream processing with Roboflow machine learning & computer vision models
- **Video Processing Workflows**: FFmpeg integration for stream conversion and frame extraction
- **Machine Learning Model Testing**: Real-time inference validation and performance optimization
- **Data Collection**: Automated frame extraction for model training dataset creation

## Project Structure

```
scripts/
├── CV_pipeline_TEST.py      # Live HLS stream processing with Roboflow inference
├── CV_pipeline_TEST2.py     # Local video file processing and output generation
├── frame_extraction.py      # Video download and frame extraction for training data
└── README.md               # This documentation file
```

## Development Pipeline

These scripts represent the phases of development:

```
Phase 1: Data Collection
├── frame_extraction.py
└── Purpose: Collect training images from recorded surf videos

Phase 2: Model Testing
├── CV_pipeline_TEST2.py
└── Purpose: Test ML model on local video files

Phase 3: Live Stream Integration
├── CV_pipeline_TEST.py
└── Purpose: Real-time HLS stream processing prototype
```

## Script Details

### `CV_pipeline_TEST.py` - Live Stream Processing Prototype

**Purpose**: This script was the foundation for the live stream processing functionality now integrated into the main application's `LiveStreamAnalyzer` class.

**Key Features**:
- **HLS to MJPEG Conversion**: Uses FFmpeg to convert HLS streams to MJPEG (Motion JPEG) format
- **Real-time Machine Learning Inference**: Integrates with Roboflow's InferencePipeline for live surfer detection
- **HTTP Stream Server**: Creates a local HTTP server for processed video streams
- **Concurrent Processing**: Handles both video conversion and Machine Learning inference simultaneously

**Technical Implementation**:
```python
class HLSToRoboflowPipeline:
    def __init__(self, hls_url, workspace_name, workflow_id, api_key):
        # Initialize pipeline with Roboflow credentials
        
    def start_ffmpeg_conversion(self):
        # Convert HLS to MJPEG using optimized FFmpeg parameters
        
    def start_roboflow_pipeline(self):
        # Initialize Roboflow inference pipeline
        
    def roboflow_sink(self, result, video_frame):
        # Process ML inference results
```

**Evolution to Production**: This prototype directly influenced the design of the production `LiveStreamAnalyzer` class in `backend/analysis/live_stream_analyzer.py`.

### `CV_pipeline_TEST2.py` - Local Video Processing

**Purpose**: Developed to test the machine learning model performance on local video files and generate processed output videos.

**Key Features**:
- **Local Video Processing**: Processes MP4 files with Roboflow inference
- **Visualization Output**: Generates videos with detection bounding boxes and labels
- **Performance Validation**: Tests model accuracy and processing speed
- **Desktop Integration**: Automatically saves processed videos to desktop

**Technical Implementation**:
```python
def my_sink(result, video_frame):
    vis_image = result.get("detection_visualization")
    if vis_image:
        frame = vis_image.numpy_image
        cv2.imshow("Workflow Image", frame)
        cv2.waitKey(1)
        out.write(frame)  # Save frame to video file
```

**Development Value**: This script was crucial for validating the custom-trained model's performance (65.4% mAP@50, 69.3% precision, 63.9% recall) before deploying to live surf cameras.

### `frame_extraction.py` - Training Data Collection

**Purpose**: Automated collection of surf video frames from video URL to create the training dataset for the custom Roboflow model.

**Key Features**:
- **YouTube Video Download**: Uses yt-dlp for high-quality video downloads
- **Automated Frame Extraction**: FFmpeg-based frame extraction at configurable intervals
- **Batch Processing**: Handles multiple video URLs simultaneously
- **Desktop Notifications**: Windows toast notifications for completion status

**Technical Implementation**:
```python
# YouTube download configuration
ydl_options = {
    'format': 'bestvideo[ext=mp4]',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'quiet': False,
    'no_warnings': True,
}

# FFmpeg frame extraction
command = [
    'ffmpeg',
    '-ss', start_time,      # Start time
    '-t', duration,         # Duration
    '-i', filename,         # Input video
    '-vf', 'fps=0.5',      # Extract at 0.5 FPS
    frame_pattern          # Output pattern
]
```

**Dataset Creation**: This script helped create the 200+ annotated surf images used to train the custom surfer detection model.

## Usage Examples

### Live Stream Testing
```bash
# Set up environment variables
export ROBOFLOW_API_KEY="your_api_key"
export ROBOFLOW_WORKSPACE="your_workspace"
export ROBOFLOW_WORKFLOW_ID="your_workflow_id"

# Run live stream processing test
python CV_pipeline_TEST.py

# View the processed stream
# Navigate to: http://localhost:8554/stream.mjpeg
```

### Local Video Processing
```bash
# Update video path in script
video_path = "path/to/your/video.mp4"

# Run local video processing
python CV_pipeline_TEST2.py

# Output will be saved to Desktop/output.mp4
```

### Frame Extraction for Training
```bash
# Update video URLs in script
vid_urls = ['https://www.youtube.com/watch?v=your_video_id']

# Run frame extraction
python frame_extraction.py

# Frames will be saved to frames/ directory
```

## Dependencies

### Python Packages
```bash
pip install opencv-python
pip install inference
pip install python-dotenv
pip install yt-dlp
pip install win10toast  # Windows only
```

### System Requirements
- **FFmpeg**: Required for video processing and frame extraction
- **Python 3.8+**: Core runtime environment
- **Roboflow Account**: API access for machine learning inference
- **Sufficient Storage**: For video downloads and frame extraction

### Installation
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install FFmpeg (Ubuntu/Debian)
sudo apt update && sudo apt install ffmpeg

# Install FFmpeg (macOS)
brew install ffmpeg

# Install FFmpeg (Windows)
# Download from https://ffmpeg.org/download.html
```

## Integration with Main Application

### Script Evolution to Production Code

**CV_pipeline_TEST.py** → **backend/analysis/live_stream_analyzer.py**
- Evolved into the production `LiveStreamAnalyzer` class
- Added robust error handling and process management
- Integrated with Flask API endpoints
- Enhanced with health monitoring and automatic recovery

**CV_pipeline_TEST2.py** → **Model Validation Framework**
- Provided foundation for model performance testing
- Influenced the design of the video processing pipeline

**frame_extraction.py** → **Training Data Pipeline**
- Created the dataset used for custom model training
- Established the frame extraction methodology
- Influenced the frame processing intervals in production

### Key Design Patterns Transferred

1. **Asynchronous Processing**: Threading patterns from test scripts
2. **Error Handling**: Robust process management and cleanup
3. **Stream Conversion**: FFmpeg parameter optimization
4. **ML Integration**: Roboflow API integration patterns

## Development Workflow

### Iterative Development Process

1. **Data Collection Phase**
   ```bash
   # Extract frames from surf videos
   python frame_extraction.py
   
   # Manually annotate extracted frames in Roboflow
   # Train custom surfer detection model
   ```

2. **Model Validation Phase**
   ```bash
   # Test model on local videos
   python CV_pipeline_TEST2.py
   
   # Analyze detection accuracy and performance
   # Iterate on model training if needed
   ```

3. **Live Stream Integration Phase**
   ```bash
   # Test real-time stream processing
   python CV_pipeline_TEST.py
   
   # Optimize FFmpeg parameters for performance
   # Validate ML inference on live streams
   ```

4. **Production Integration**
   ```bash
   # Integrate tested components into main application
   # Add API endpoints and error handling
   # Deploy to production environment
   ```

### Performance Optimization Journey

- **Initial Frame Rate**: 5 FPS processing
- **Stream Resolution**: 1280x720 optimization
- **FFmpeg Parameters**: Ultrafast preset for real-time processing

## Troubleshooting

### Common Issues and Solutions

#### FFmpeg Not Found
```bash
# Verify FFmpeg installation
ffmpeg -version

# Add FFmpeg to PATH (Windows)
# Add installation directory to system PATH

# Install via package manager (Linux/macOS)
sudo apt install ffmpeg  # Ubuntu/Debian
brew install ffmpeg      # macOS
```

#### Stream Connection Issues
```bash
# Test stream accessibility
ffmpeg -i "https://your-stream-url.com/playlist.m3u8" -t 10 test.mp4

# Check network connectivity
ping your-stream-domain.com

# Verify stream format
curl -I "https://your-stream-url.com/playlist.m3u8"
```

#### Roboflow API Issues
```bash
# Test API key validity
python -c "from inference import InferencePipeline; print('API key valid')"

# Check workspace and workflow IDs
# Verify model deployment status in Roboflow dashboard
```

#### Memory Issues
```bash
# Monitor memory usage during processing
htop  # Linux/macOS
taskmgr  # Windows

# Reduce frame rate if memory constrained
# Modify fps parameter in FFmpeg command
```

## Future Enhancements

### Integration Opportunities

- **CI/CD Pipeline**: Automated testing with these scripts
- **Model Evaluation**: Continuous model performance validation
- **Data Pipeline**: Automated training data collection and processing
- **Monitoring**: Real-time system health and performance tracking

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

________________________________________
Built with ❤️ for the surfing community

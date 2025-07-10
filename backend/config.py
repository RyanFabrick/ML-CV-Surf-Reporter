import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """
    config class for Flask application
    """
    
    #rboflow API settings
    ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
    ROBOFLOW_WORKSPACE = os.getenv("ROBOFLOW_WORKSPACE")
    ROBOFLOW_WORKFLOW_ID = os.getenv("ROBOFLOW_WORKFLOW_ID")
    
    #flask settings
    DEBUG = True
    
    #analysis settings
    MAX_FPS = 2
    BASE_PORT = 8550
    
    #FFmpeg settings
    FFMPEG_QUALITY = 2
    FFMPEG_RESOLUTION = '1280x720'
    FFMPEG_TIMEOUT = 10
    
    #update intervals (in seconds)
    WAVE_UPDATE_INTERVAL = 180  #3 minutes
    VIDEO_UPDATE_INTERVAL = 5   #5 seconds
    HEALTH_CHECK_INTERVAL = 5   #5 seconds
import threading
import time
import subprocess
import traceback
from datetime import datetime
from inference import InferencePipeline
from config import Config

class LiveStreamAnalyzer:
    def __init__(self, webcam_id, hls_url):
        self.webcam_id = webcam_id
        self.hls_url = hls_url
        self.ffmpeg_process = None
        self.pipeline = None
        self.port_number = Config.BASE_PORT + int(webcam_id) if webcam_id.isdigit() else Config.BASE_PORT + 1
        self.stream_url = f"http://localhost:{self.port_number}/stream.mjpeg"
        self.latest_result = {
            'surfer_count': 0,
            'status': 'Starting',
            'last_update': None
        }
    
    def roboflow_sink(self, result, video_frame):
        #processes results from CV inference (roboflow)
        try:
            #intializes surfer count
            surfer_count = 0
            #debugging - type of data received
            print(f"Result type: {type(result)}")
            
            data = result
            #Checks if 'result' is a tuple
            if isinstance(result, tuple):
                print(f"Tuple length: {len(result)}")
                data = result[0]
            
            #Checks if data is 'dict' and 'predicitons' key exists
            if isinstance(data, dict) and 'predictions' in data:
                print(f"Found predictions, count: {len(data['predictions'])}")

                #loops through each prediciton
                #enumerate gives index and item
                for i, prediction in enumerate(data['predictions']):
                    print(f"Prediction {i} type: {type(prediction)}")
                    # checks if prediciton is tuple
                    if isinstance(prediction, tuple) and len(prediction) >= 6:
                        print(f"Prediction is tuple with {len(prediction)} elements")
                        #extracts metadata and gets surfer count
                        metadata = prediction[5] if len(prediction) > 5 else {}
                        #checks if metadata is dict
                        if isinstance(metadata, dict):
                            #extracts class_name
                            class_name = metadata.get('class_name', '')
                            print(f"Class name from metadata: {class_name}")
                            #checks if class_name is 'Surfer'
                            #increments counter accordingly
                            if class_name.lower() == 'surfer':
                                surfer_count += 1
                    #alternative, checks if prediciton is dict
                    elif isinstance(prediction, dict):
                        #checks class_name
                        class_name = prediction.get('class', prediction.get('class_name', ''))
                        print(f"Class name from dict: {class_name}")
                        #checks if class_name is 'Surfer
                        #increments counter accordingly
                        if class_name.lower() == 'surfer':
                            surfer_count += 1
            else:
                #debugging print if DS is unexpected
                print(f"Data is not a dict with predictions: {type(data)}")

            #updates latest result
            self.latest_result = {
                'surfer_count': surfer_count,
                'status': 'online',
                'last_update': datetime.now().isoformat()
            }

            # Import here to avoid circular imports
            from routes.video_analysis import analysis_results
            #stores global results
            analysis_results[self.webcam_id] = self.latest_result
            print(f"Updated Analysis for {self.webcam_id}: {surfer_count} surfers detected")

        except Exception as e:
            print(f"Error Processing Result: {e}")
            print(f"Error location: {traceback.format_exc()}")
            self.latest_result['status'] = 'error'

    def check_ffmpeg_process(self):
        if self.ffmpeg_process and self.ffmpeg_process.poll() is not None:
            print("FFmpeg process died, restarting...")
            try:
                # Clean up old process
                if self.ffmpeg_process:
                    self.ffmpeg_process.terminate()
                    self.ffmpeg_process.wait(timeout=5)
                
                # Restart
                if not self.start_ffmpeg_conversion():
                    print("Failed to restart FFmpeg")
                    self.latest_result['status'] = 'ffmpeg_error'
                else:
                    print("FFmpeg restarted successfully")
                    self.latest_result['status'] = 'online'
                    
            except Exception as e:
                print(f"Error restarting FFmpeg: {e}")
                self.latest_result['status'] = 'error'

    def start_ffmpeg_conversion(self):
        ffmpeg_commands = [
            'ffmpeg',
            '-re',  # Read input at native frame rate
            '-i', self.hls_url,
            '-f', 'mjpeg',
            '-r', str(Config.MAX_FPS),
            '-s', Config.FFMPEG_RESOLUTION,
            '-q:v', str(Config.FFMPEG_QUALITY),  # Quality level (2-31, lower is better)
            '-listen', '1',
            '-timeout', str(Config.FFMPEG_TIMEOUT),  # Timeout after 10 seconds of no connection
            '-analyzeduration', '1000000',  # Faster stream analysis
            '-probesize', '1000000',
            '-y',
            self.stream_url
        ]
        
        try:
            print(f"Starting FFmpeg Conversion for {self.webcam_id} on {self.stream_url}")
            self.ffmpeg_process = subprocess.Popen(
                ffmpeg_commands,
                stderr=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL
            )
            return True
        except Exception as e:
            print(f"Error Starting FFmpeg for {self.webcam_id}: {e}")
            return False
    
    def start_roboflow_pipeline(self):
        #starts Roboflow inference pipeline
        try:
            print(f"Connecting to stream: {self.stream_url}")
            self.pipeline = InferencePipeline.init_with_workflow(
                api_key=Config.ROBOFLOW_API_KEY,
                workspace_name=Config.ROBOFLOW_WORKSPACE,
                workflow_id=Config.ROBOFLOW_WORKFLOW_ID,
                video_reference=self.stream_url, 
                max_fps=Config.MAX_FPS,
                on_prediction=self.roboflow_sink
            )

            time.sleep(5)

            print("Starting Roboflow Pipeline for {self.webcam_id}...")
            self.pipeline.start()
            return True
        except Exception as e:
            print(f"Error Starting Roboflow Pipeline: for {self.webcam_id}: {e}")
            return False
        
    def start_analysis(self):
        print(f"Starting analysis for webcam: {self.webcam_id}")
        print(f"HLS URL: {self.hls_url}")

        def run_pipeline():
            try:
                if not self.start_ffmpeg_conversion():
                    self.latest_result['status'] = 'ffmpeg_error'
                    return
                
                # Start health check thread
                health_thread = threading.Thread(target=self.health_check, daemon=True)
                health_thread.start()

                if not self.start_roboflow_pipeline():
                    self.latest_result['status'] = 'roboflow_error'
                    return
                
                self.pipeline.join()
                
            except Exception as e:
                print(f"Pipeline Error for {self.webcam_id}: {e}")
                self.latest_result['status'] = 'error'

        thread = threading.Thread(target=run_pipeline, daemon=True)
        thread.start()
        return thread

    def health_check(self):
        """Continuously check FFmpeg and restart if needed"""
        while True:
            time.sleep(Config.HEALTH_CHECK_INTERVAL)  # Check every 5 seconds
            self.check_ffmpeg_process()
            
            # Also check if Roboflow is still connected
            if self.pipeline and not self.pipeline.is_running():
                print("Roboflow pipeline stopped, attempting to restart...")
                self.start_roboflow_pipeline()
    
    def stop_analysis(self):
        #stops analysis pipeline
        if self.pipeline:
            self.pipeline.terminate()
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
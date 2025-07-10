import threading #enables concurrent execution for running multiple streams simultaneously
import time #time related functions (delays, etc)
import subprocess #enables spawning of new processes (for FFmpeg vid conversion)
import traceback #for debugging - detailed error info
from datetime import datetime #timestamping analysis results
from inference import InferencePipeline #roboflow's inference pipeline for object detection
from config import Config #configuration settings (API keys, ports, etc)

class LiveStreamAnalyzer:
    """
    main class responsible for analyzing live vid streams to detect surfers
    ffmpeg process -> convers HLS to MJPEG
    #roboflow pipeline -> inference to detect surfers
    #results management -> stores and updates detection results
    """
    def __init__(self, webcam_id, hls_url):
        """
        initlaizes live stream analyzer for specific webcam (surfcam)
        webcam_id -> unique identifier for webcam
        hls_url -> HLS url from webcam source
        sets up stream conversion params, por allocation for local MJPEG stream, inital result state
        """
        self.webcam_id = webcam_id #unique id for webcam instance
        self.hls_url = hls_url #source webcam HLS url
        self.ffmpeg_process = None #will hold ffmpeg subprocess
        self.pipeline = None #will hold roboflow inference pipeline
        #unique port for webcam's local mjpeg stream
        self.port_number = Config.BASE_PORT + int(webcam_id) if webcam_id.isdigit() else Config.BASE_PORT + 1
        self.stream_url = f"http://localhost:{self.port_number}/stream.mjpeg"
        self.latest_result = {
            'surfer_count': 0,
            'status': 'Starting',
            'last_update': None
        }
    
    #
    def roboflow_sink(self, result, video_frame):
        """
        callback function processes results from roboflow inference
        result -> inference result containing detection data
        video_frame -> actual vid frame
        handles tuples, dicts
        """
        try:
            #intializes surfer count
            surfer_count = 0
            #debugging - data structure received
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
        """
        monitors FFmpeg process health, restarts if necessary
        called by health check thread
        """
        #checks if ffmpeg process has terminated poll() returns none if running
        if self.ffmpeg_process and self.ffmpeg_process.poll() is not None:
            print("FFmpeg process died, restarting...")
            try:
                #clean up old process
                if self.ffmpeg_process:
                    self.ffmpeg_process.terminate()
                    self.ffmpeg_process.wait(timeout=5)
                
                #restarts ffmpeg
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
        """
        starts ffmpeg process to conver HLS stream to mjpeg
        returns bool: true if ffmpef started successfuly
        returns bool: false otherwise
        """
        #command configurations
        ffmpeg_commands = [
            'ffmpeg',
            '-re',  #read input at native frame rate
            '-i', self.hls_url, #input
            '-f', 'mjpeg', #output
            '-r', str(Config.MAX_FPS), #frame rate limit
            '-s', Config.FFMPEG_RESOLUTION, #vid res
            '-q:v', str(Config.FFMPEG_QUALITY),  #quality level (2-31, lower is better)
            '-listen', '1', #enables http server mode
            '-timeout', str(Config.FFMPEG_TIMEOUT),  #timeout after 10 seconds of no connection
            '-analyzeduration', '1000000',  #faster stream analysis
            '-probesize', '1000000', #limits probe size, faster startup
            '-y', #overwrite output
            self.stream_url #output: local mjpeg stream url
        ]
        
        try:
            print(f"Starting FFmpeg Conversion for {self.webcam_id} on {self.stream_url}")
            #starts ffmpeg as subprocess with output suppressed
            self.ffmpeg_process = subprocess.Popen(
                ffmpeg_commands,
                stderr=subprocess.DEVNULL, #suppress error output
                stdout=subprocess.DEVNULL  #supress standard output
            )
            return True
        except Exception as e:
            print(f"Error Starting FFmpeg for {self.webcam_id}: {e}")
            return False
    
    def start_roboflow_pipeline(self):
        """
        initialzies and starts roboflow inference pipeline
        returns bool: true if pipeline started successfuly
        returns bool: false otherwise
        """
        try:
            print(f"Connecting to stream: {self.stream_url}")
            #intilaizes roboflow pipeline w/ configurations
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
        """
        main method to start complete analysis pipeline
        starts ffmpeg for stream conversion
        launches health monitoring
        starts roboflow processing
        handles errors
        runs in separate thread
        returns threading.Thread: The thread running the analysis pipeline
        """
        print(f"Starting analysis for webcam: {self.webcam_id}")
        print(f"HLS URL: {self.hls_url}")

        def run_pipeline():
            """
            internal function runs the complete pipeline
            in a separate thread to prevent blocking
            """
            try:
                #step 1 - starts conversion
                if not self.start_ffmpeg_conversion():
                    self.latest_result['status'] = 'ffmpeg_error'
                    return
                
                #step 2 - starts health monitoring
                health_thread = threading.Thread(target=self.health_check, daemon=True)
                health_thread.start()

                #step 3 - starts roboflow process
                if not self.start_roboflow_pipeline():
                    self.latest_result['status'] = 'roboflow_error'
                    return
                
                #step 4 - keeps pipeline running
                self.pipeline.join()
                
            except Exception as e:
                print(f"Pipeline Error for {self.webcam_id}: {e}")
                self.latest_result['status'] = 'error'

        #starts piepline in daemon thread
        #daemon threads auto exit when main progmram exits
        thread = threading.Thread(target=run_pipeline, daemon=True)
        thread.start()
        return thread

    def health_check(self):
        """
        continuously check FFmpeg and restart if needed
        runs in background thread
        checks ffmpeg process health
        monitors roboflow pipeline status
        auto restarts failed parts
        prevents hanging on failures
        runs indef until thread is terminated
        """
        while True:
            #check every 5 seconds
            time.sleep(Config.HEALTH_CHECK_INTERVAL)
            self.check_ffmpeg_process()
            
            #check if Roboflow is still connected
            if self.pipeline and not self.pipeline.is_running():
                print("Roboflow pipeline stopped, attempting to restart...")
                self.start_roboflow_pipeline()
    
    def stop_analysis(self):
        """
        clean shutfown of analysis pipeline
        terminates roboflow pipeline
        stops ffmpeg process
        cleans system reosurces
        prevents resource leaks
        called when stopping analysis for webcam or applciation shutdown
        """

        #stops roboflow inference pipeline
        if self.pipeline:
            self.pipeline.terminate()
        
        #stops ffmpeg conversion rpocess
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
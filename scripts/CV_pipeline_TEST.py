import subprocess
import threading
import time
import tempfile
import os
from inference import InferencePipeline
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ROBOFLOW_API_KEY")
workspace_name = os.getenv("ROBOFLOW_WORKSPACE")
workflow_id = os.getenv("ROBOFLOW_WORKFLOW_ID")


#ffmpeg -allowed_extensions ALL -protocol_whitelist file,http,https,tcp,tls -i "https://hls.cdn-surfline.com/oregon/wc-leadbetter/playlist.m3u8" -f mjpeg -r 5 -s 1280x720 -listen 1 http://localhost:8554/stream.mjpeg
#ffmpeg -i "https://windansea.b-cdn.net/sunba/windansea/chunklist.m3u8" -f mjpeg -r 5 -s 1280x720 -listen 1 http://localhost:8554/stream.mjpeg

class HLSToRoboflowPipeline:

    def __init__(self, hls_url, workspace_name, workflow_id, api_key):
        self.hls_url = hls_url
        self.api_key = api_key
        self.workspace_name = workspace_name
        self.workflow_id = workflow_id
        self.ffmpeg_process = None
        self.pipeline = None
        self.stream_url = "http://localhost:8554/stream.mjpeg"

    # def create_named_pipe(self):
    #     try:
    #         if os.name == 'nt':
    #             self.pipe_path = "temp_stream.mkv"
    #             return True
    #         else:
    #             os.mkfifo(self.pipe_path)
    #             return True
    #     except Exception as e:
    #         print(f"Error Creating Pipe: {e}")
    #         return False
    
    def start_ffmpeg_conversion(self):

        ffmpeg_commands = [
            
            'ffmpeg',
            '-i', self.hls_url,           # Input: your HLS URL
            '-f', 'mjpeg',             # Output format 
            # '-vcodec', 'libx264',         # Video codec
            # '-preset', 'ultrafast',       # Fast encoding for real-time
            # '-tune', 'zerolatency',       # Minimize latency
            '-r', '5',                   # Frame rate 
            '-s', '1280x720',             # Resolution
            '-listen', '1',               # Listen for incoming connections
            '-y',                         # Overwrite output
            self.stream_url               # Output to our pipe
        ]
        
        try:
            print(f"Starting FFmpeg Conversion From {self.hls_url}")
            print(f"Stream will be available at: {self.stream_url}")
            self.ffmpeg_process = subprocess.Popen(
                ffmpeg_commands,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            return True
        except Exception as e:
            print(f"Error Starting FFmpeg: {e}")
            return False
        
    def roboflow_sink(self, result, video_frame):
        if result.get("output_image"):
            print("Frame Processed by Roboflow")
        print(f"Detection Results: {result}")

    def start_roboflow_pipeline(self):
        try:
            print(f"Connecting to stream: {self.stream_url}")
            self.pipeline = InferencePipeline.init_with_workflow(
                api_key=self.api_key,
                workspace_name=self.workspace_name,
                workflow_id=self.workflow_id,
                video_reference=self.stream_url, 
                max_fps=5,
                on_prediction=self.roboflow_sink
            )

            print("Waiting for FFmpeg HTTP server to start...")
            time.sleep(5)

            print("Starting Roboflow Pipeline...")
            self.pipeline.start()
            return True
        except Exception as e:
            print(f"Error Starting Roboflow Pipeline: {e}")
            return False
    
    def run(self):
        print("Setting Up HLS to Roboflow Pipeline...")

        # if not self.create_named_pipe():
        #     print("Failed to Create Pipe")
        #     return False
         
        if not self.start_ffmpeg_conversion():
            print("Failed to Start FFmpeg Conversion")
            return False
        
        if not self.start_roboflow_pipeline():
            print("Failed to Start Roboflow Pipeline")
            return False
        
        try:
            print("Pipeline running - Ctrl+C to Stop")
            print("You can also view the stream at: http://localhost:8554/stream.mjpeg")
            self.pipeline.join()
        except KeyboardInterrupt:
            print("Stopping Pipeline...")
        finally:
            self.cleanup()
        
    def cleanup(self):
        print("Cleaning up...")
        if self.pipeline:
            self.pipeline.terminate()
        
        if self.ffmpeg_process:
            self.ffmpeg_process.terminate()
            self.ffmpeg_process.wait()
        
        # try:
        #     if os.path.exists(self.pipe_path):
        #         os.remove(self.pipe_path)
        # except:
        #     pass
if __name__ == "__main__":

    hls_url = "https://windansea.b-cdn.net/sunba/windansea/chunklist.m3u8"

    converter = HLSToRoboflowPipeline(
        hls_url,
        workspace_name,
        workflow_id,
        api_key
    )
    
    converter.run()


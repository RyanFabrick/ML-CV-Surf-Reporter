import xarray as xr
import urllib.request
import pandas as pd
import threading
import time
import subprocess
import os
import numpy as np
import cv2
import traceback
from flask import Flask, jsonify, request, render_template, Response
from flask_cors import CORS
from datetime import datetime, timezone
from inference import InferencePipeline
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("ROBOFLOW_API_KEY")
workspace_name = os.getenv("ROBOFLOW_WORKSPACE")
workflow_id = os.getenv("ROBOFLOW_WORKFLOW_ID")

app = Flask(__name__)
CORS(app)

#global vars store analysis results
analysis_results = {}
active_pipelines = {}

class LiveStreamAnalyzer:
    def __init__(self, webcam_id, hls_url):
        self.webcam_id = webcam_id
        self.hls_url = hls_url
        self.ffmpeg_process = None
        self.pipeline = None
        self.port_number = 8550 + int(webcam_id) if webcam_id.isdigit() else 8551
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
            '-r', '2',
            '-s', '1280x720',
            '-q:v', '2',  # Quality level (2-31, lower is better)
            '-listen', '1',
            '-timeout', '10',  # Timeout after 10 seconds of no connection
            '-analyzeduration', '1000000',  # Faster stream analysis
            '-probesize', '1000000',
            '-y',
            self.stream_url
        ]
        
        try:
            print(f"Starting FFmpeg Conversion for {self.webcam_id} on {self.stream_url}")
            with open(f'ffmpeg_{self.webcam_id}.log', 'w') as log_file:
                self.ffmpeg_process = subprocess.Popen(
                    ffmpeg_commands,
                    stderr=log_file,
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
                api_key=api_key,
                workspace_name=workspace_name,
                workflow_id=workflow_id,
                video_reference=self.stream_url, 
                max_fps=2,
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
            time.sleep(5)  # Check every 5 seconds
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

#webcam configurations (modified later)
Webcam_Configs = {
    'malibu': {
        'name': 'Malibu - Point Dume',
        'location': 'Malibu, CA',
        'hls_url': 'https://windansea.b-cdn.net/sunba/windansea/chunklist.m3u8',
        'buoy_nearby': '273'
    }
}

@app.route('/')
def serve_frontend():
    return render_template('frontend.html')

@app.route('/api/video-analysis')
def get_video_analysis():
    #gets webcam_id from query parameters

    try:
        webcam_id = request.args.get('webcam_id')
        print(f"Received webcam_id: {webcam_id}")

        #checks if webcam_id is provided and valid
        if not webcam_id:
            return jsonify({'error': 'No Webcam Selected'}), 400
        if webcam_id not in Webcam_Configs: #will upgrade later
            return jsonify({'error': 'Webcam Not Available'}), 404
        
        #analysis starts IF not running already
        if webcam_id not in active_pipelines:
            config = Webcam_Configs[webcam_id]
            analyzer = LiveStreamAnalyzer(webcam_id, config['hls_url'])
            active_pipelines[webcam_id] = analyzer
            analyzer.start_analysis()

            #returns intial status
            return jsonify({
                'webcam_id': webcam_id,
                'location_name': config['name'],
                'surfer_count': 0,
                'status': 'Starting',
                'message': 'Analysis Starting, Please Wait...'
            })
        
        #gets latest analysis results
        if webcam_id in analysis_results:
            result = analysis_results[webcam_id]
            config = Webcam_Configs[webcam_id]

            return jsonify({
                'webcam_id': webcam_id,
                'location_name': config['name'],
                'surfer_count': result['surfer_count'],
                'status': result['status'],
                'last_update': result['last_update']
            })
        else:
            return jsonify({
                'webcam_id': webcam_id,
                'location_name': Webcam_Configs[webcam_id]['name'],
                'surfer_count': 0,
                'status': 'Initializing'
            })
    
    except Exception as e:
        print(f"ERROR in video_analysis route: {e}")
        print(f"Error type: {type(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop-analysis/<webcam_id>')
def stop_analysis(webcam_id):
    #Stops analysis for SPECIFIC webcam_id
    if webcam_id in active_pipelines:
        active_pipelines[webcam_id].stop_analysis()
        del active_pipelines[webcam_id]
        if webcam_id in analysis_results:
            del analysis_results[webcam_id]
        return jsonify({'message': f'Analysis Stopped for {webcam_id}'})
    return jsonify({'error': 'No Active Analysis Found'}), 404

@app.route('/video_feed/<webcam_id>')
def video_feed(webcam_id):
    if webcam_id not in active_pipelines:
        return "Webcam not active", 404
    
    try:
        # This is a simple proxy to the MJPEG stream
        stream_url = active_pipelines[webcam_id].stream_url
        resp = urllib.request.urlopen(stream_url)
        return Response(resp.read(), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as e:
        print(f"Video feed error: {e}")
        return "Stream unavailable", 503

#Exisitng surfdata route accepts bupy_id parameter
@app.route('/api/surfdata')
def get_surf_data():
    
    #gets buoy_id from query parameters, default - 237(point dume)
    buoy_id = request.args.get('buoy_id', '273')
    
    try:    
        # Step 1: ppoint to public netCDF file for data 
        # (Point Dume Bouy - 273)
        url = f'https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/{buoy_id}p1_rt.nc'

        # checks connectivity to CDIP server
        #try:
        #    urllib.request.urlopen(url, timeout=30)
        #except Exception as e:
        #    return jsonify({'error': 'CDIP Server Unreachable', 'Details': str(e)}), 504

        # loads .nc file directly
        #ds = xr.open_dataset('273p1_rt.nc')

        # opens dataset remotely
        ds = xr.open_dataset(url)

        ds = ds.isel(waveTime=slice(-30, None))

        # Step 2: filter for "good" records
        # CDIP documentation reccomenndation
        # keeps only "good" records
        good = ds['waveFlagPrimary'] == 1
        ds = ds.where(good, drop=True)
        if ds.waveTime.size == 0:
            return jsonify({'error': 'No Valid Wave Data Found'}), 404

        # Step 3: Extract relevant data
        # Relevant data: time, 
        # wave height significant (waveHs),
        # peak wave period (waveTp),
        # peak wave direction (waveDp),
        # avg wave period (waveTa),
        # mean zero-upcrossing period (waveTz),
        # peak wave power spectral density (wavePeakPSD)
        times = ds['waveTime'].values[:10]
        wave_height_significant = ds['waveHs'].values[:10]
        wave_tp = ds['waveTp'].values[:10]
        wave_dp = ds['waveDp'].values[:10]
        wave_ta = ds['waveTa'].values[:10]
        wave_tz = ds['waveTz'].values[:10]
        wave_psd = ds['wavePeakPSD'].values[:10]

        # Step 4: convert UNIX to readable format
        #converts numpy.datetime64 to Python datetime/format, each
        readable_time = []
        for t in times:
            #converts to pandas.Timestamp
            timestamp = pd.to_datetime(t)
            #formats as 'YYY-MM-DD HH:MM'
            formatted = timestamp.strftime('%Y-%m-%d %H:%M')
            #appends to list
            readable_time.append(formatted)

        # Step 5: returns data to frontend as JSON
        return jsonify({

            'time': readable_time,
            "waveHs": wave_height_significant.tolist(),
            "waveTp": wave_tp.tolist(),
            "waveDp": wave_dp.tolist(),
            "waveTa": wave_ta.tolist(),
            "waveTz": wave_tz.tolist(),
            "wavePeakPSD": wave_psd.tolist()

        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug = True)
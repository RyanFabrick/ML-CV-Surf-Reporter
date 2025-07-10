import urllib.request #for http request to proxy mjpeg vid streams
                        #for backend to fetch from local ffmpeg streams
                        #serves to frontend w/o direct access
import traceback
from flask import Blueprint, jsonify, request, Response
from analysis.live_stream_analyzer import LiveStreamAnalyzer
from webcam_configs import WEBCAM_CONFIGS

video_analysis_bp = Blueprint('video_analysis', __name__)

#global dicts data between http requests
analysis_results = {} #latest detection results
active_pipelines = {} #maintains references to active LiveStreamAnalyzer instances

@video_analysis_bp.route('/api/video-analysis')
def get_video_analysis():
    """
    main api endpoint for retreiving vid analysis data
    and managing analysis pipelines

    returns JSON with webcam info, surfer count, status, timestamp
    error response for invalid request or system fails
    """
    try:
        webcam_id = request.args.get('webcam_id')
        print(f"Received webcam_id: {webcam_id}")

        #checks if webcam_id is provided and valid
        if not webcam_id:
            return jsonify({'error': 'No Webcam Selected'}), 400
        if webcam_id not in WEBCAM_CONFIGS: #will upgrade later
            return jsonify({'error': 'Webcam Not Available'}), 404
        
        #analysis starts IF not running already
        if webcam_id not in active_pipelines:
            config = WEBCAM_CONFIGS[webcam_id]
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
            config = WEBCAM_CONFIGS[webcam_id]

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
                'location_name': WEBCAM_CONFIGS[webcam_id]['name'],
                'surfer_count': 0,
                'status': 'Initializing'
            })
    
    except Exception as e:
        print(f"ERROR in video_analysis route: {e}")
        print(f"Error type: {type(e)}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@video_analysis_bp.route('/api/stop-analysis/<webcam_id>')
def stop_analysis(webcam_id):
    """
    api endpoint to stop vid analysis for specifci webcam 
    webcam_id -> URL paramrter for specific webcam
    returns success if pipeline stopped succesffuly
    returns error if no active piepline found
    """

    #checks if active pipeline exists
    if webcam_id in active_pipelines:
        active_pipelines[webcam_id].stop_analysis()
        del active_pipelines[webcam_id]
        if webcam_id in analysis_results:
            del analysis_results[webcam_id]
        return jsonify({'message': f'Analysis Stopped for {webcam_id}'})
    return jsonify({'error': 'No Active Analysis Found'}), 404

@video_analysis_bp.route('/video_feed/<webcam_id>')
def video_feed(webcam_id):
    """
    vid streaming enpoint that proxies mjpeg streams to frontend
    webcam_id -> URL paramrter for specific webcam
    returns streaming response with mjpeg vid data
    returns error for inactive webcams, stream failures
    """

    #verifies analysis pipeline is active for webcam
    if webcam_id not in active_pipelines:
        return "Webcam not active", 404
    
    try:
        #simple proxy to the MJPEG stream
        stream_url = active_pipelines[webcam_id].stream_url
        resp = urllib.request.urlopen(stream_url)
        return Response(resp.read(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
    except Exception as e:
        print(f"Video feed error: {e}")
        return "Stream unavailable", 503
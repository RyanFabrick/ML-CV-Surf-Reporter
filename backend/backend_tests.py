import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import threading
import time
from datetime import datetime
import subprocess
import sys
import os

#adds backend directory to the Python path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from analysis.live_stream_analyzer import LiveStreamAnalyzer
from routes.video_analysis import video_analysis_bp, analysis_results, active_pipelines
from routes.surf_data import surf_data_bp
from routes.frontend import frontend_bp
from config import Config
from webcam_configs import WEBCAM_CONFIGS
from app import create_app


class TestConfig(unittest.TestCase):
    """
    tests for config settings and environment variables
    ensures application can properly load and access config values
    """
    
    def test_config_has_required_attributes(self):
        """
        tests Config class contains all required configuration attributes
        ensures application won't crash due to missing configuration values
        """
        #tests all required Roboflow settings exist
        self.assertTrue(hasattr(Config, 'ROBOFLOW_API_KEY'))
        self.assertTrue(hasattr(Config, 'ROBOFLOW_WORKSPACE'))
        self.assertTrue(hasattr(Config, 'ROBOFLOW_WORKFLOW_ID'))
        
        #tests all required Flask settings exist
        self.assertTrue(hasattr(Config, 'DEBUG'))
        
        #tests all required analysis settings exist
        self.assertTrue(hasattr(Config, 'MAX_FPS'))
        self.assertTrue(hasattr(Config, 'BASE_PORT'))
        
        #tests all required FFmpeg settings exist
        self.assertTrue(hasattr(Config, 'FFMPEG_QUALITY'))
        self.assertTrue(hasattr(Config, 'FFMPEG_RESOLUTION'))
        self.assertTrue(hasattr(Config, 'FFMPEG_TIMEOUT'))
        
        #tests all required interval settings exist
        self.assertTrue(hasattr(Config, 'WAVE_UPDATE_INTERVAL'))
        self.assertTrue(hasattr(Config, 'VIDEO_UPDATE_INTERVAL'))
        self.assertTrue(hasattr(Config, 'HEALTH_CHECK_INTERVAL'))
    
    def test_config_values_are_reasonable(self):
        """
        tests that config values are within reasonable ranges
        prevents performance issues from misconfigured values
        """
        #tests that FPS is reasonable (1-30)
        self.assertGreaterEqual(Config.MAX_FPS, 1)
        self.assertLessEqual(Config.MAX_FPS, 30)
        
        #tests that port is in valid range
        self.assertGreaterEqual(Config.BASE_PORT, 1024)  #above reserved ports
        self.assertLessEqual(Config.BASE_PORT, 65535)    #below max ports
        
        #tests that FFmpeg quality is valid (1-31)
        self.assertGreaterEqual(Config.FFMPEG_QUALITY, 1)
        self.assertLessEqual(Config.FFMPEG_QUALITY, 31)
        
        #tests that intervals are positive
        self.assertGreater(Config.WAVE_UPDATE_INTERVAL, 0)
        self.assertGreater(Config.VIDEO_UPDATE_INTERVAL, 0)
        self.assertGreater(Config.HEALTH_CHECK_INTERVAL, 0)


class TestWebcamConfigs(unittest.TestCase):
    """
    tests for webcam config DS tuple dict etc
    """
    
    def test_webcam_configs_not_empty(self):
        """
        tests webcam configurations exist and are not empty
        """
        self.assertIsInstance(WEBCAM_CONFIGS, dict)
        self.assertGreater(len(WEBCAM_CONFIGS), 0)
    
    def test_webcam_configs_structure(self):
        """
        tests that each webcam configuration has the required fields.
        """
        for webcam_id, config in WEBCAM_CONFIGS.items():
            #each config should be a dictionary
            self.assertIsInstance(config, dict)
            
            #each config should have required fields
            self.assertIn('name', config)
            self.assertIn('location', config)
            self.assertIn('hls_url', config)
            
            #fields should be strings
            self.assertIsInstance(config['name'], str)
            self.assertIsInstance(config['location'], str)
            self.assertIsInstance(config['hls_url'], str)
            
            #URL should be a valid HTTP/HTTPS URL
            self.assertTrue(config['hls_url'].startswith(('http://', 'https://')))
    
    def test_webcam_ids_are_strings(self):
        """
        tests that webcam IDs are strings
        """
        for webcam_id in WEBCAM_CONFIGS.keys():
            self.assertIsInstance(webcam_id, str)
            self.assertGreater(len(webcam_id), 0)


class TestLiveStreamAnalyzer(unittest.TestCase):
    """
    tests for the LiveStreamAnalyzer class
    """
    
    def setUp(self):
        """
        sets up test fixtures before each test method
        creates a test analyzer instance with mock data
        """
        self.webcam_id = "test_webcam"
        self.hls_url = "https://test.example.com/stream.m3u8"
        self.analyzer = LiveStreamAnalyzer(self.webcam_id, self.hls_url)
    
    def test_analyzer_initialization(self):
        """
        tests that the LiveStreamAnalyzer initializes correctly.
        """
        #test basic attributes
        self.assertEqual(self.analyzer.webcam_id, self.webcam_id)
        self.assertEqual(self.analyzer.hls_url, self.hls_url)
        self.assertIsNone(self.analyzer.ffmpeg_process)
        self.assertIsNone(self.analyzer.pipeline)
        
        #test port calculation
        expected_port = Config.BASE_PORT + 1  # Since webcam_id is not digit
        self.assertEqual(self.analyzer.port_number, expected_port)
        
        #test stream URL construction
        expected_stream_url = f"http://localhost:{expected_port}/stream.mjpeg"
        self.assertEqual(self.analyzer.stream_url, expected_stream_url)
        
        #test initial result structure
        self.assertEqual(self.analyzer.latest_result['surfer_count'], 0)
        self.assertEqual(self.analyzer.latest_result['status'], 'Starting')
        self.assertIsNone(self.analyzer.latest_result['last_update'])
    
    def test_port_calculation_with_numeric_id(self):
        """
        tests port calculation when webcam_id is numerical
        """
        numeric_analyzer = LiveStreamAnalyzer("123", self.hls_url)
        expected_port = Config.BASE_PORT + 123
        self.assertEqual(numeric_analyzer.port_number, expected_port)
    
    @patch('subprocess.Popen')
    def test_start_ffmpeg_conversion_success(self, mock_popen):
        """
        tests successful FFmpeg process startup.
        """
        #mock successful process creation
        mock_process = Mock()
        mock_popen.return_value = mock_process
        
        #test successful start
        result = self.analyzer.start_ffmpeg_conversion()
        self.assertTrue(result)
        self.assertEqual(self.analyzer.ffmpeg_process, mock_process)
        
        #verify FFmpeg was called with correct parameters
        mock_popen.assert_called_once()
        call_args = mock_popen.call_args[0][0]  # Get the command list
        self.assertIn('ffmpeg', call_args)
        self.assertIn(self.hls_url, call_args)
        self.assertIn(self.analyzer.stream_url, call_args)
    
    @patch('subprocess.Popen')
    def test_start_ffmpeg_conversion_failure(self, mock_popen):
        """
        tests FFmpeg process startup failure handling
        """
        #mock process creation failure
        mock_popen.side_effect = Exception("FFmpeg not found")
        
        #test failed start
        result = self.analyzer.start_ffmpeg_conversion()
        self.assertFalse(result)
        self.assertIsNone(self.analyzer.ffmpeg_process)
    
    def test_roboflow_sink_with_valid_data(self):
        """
        tests the roboflow_sink callback with valid detection data
        """
        # mock result data with surfer detections
        mock_result = {
            'predictions': [
                # Mock prediction with tuple format
                (0, 0, 100, 100, 0.9, {'class_name': 'Surfer'}),
                # Mock prediction with dict format
                {'class': 'Surfer', 'confidence': 0.8}
            ]
        }
        
        #process the result
        self.analyzer.roboflow_sink(mock_result, None)
        
        #verify results were updated
        self.assertEqual(self.analyzer.latest_result['surfer_count'], 2)
        self.assertEqual(self.analyzer.latest_result['status'], 'online')
        self.assertIsNotNone(self.analyzer.latest_result['last_update'])
    
    def test_roboflow_sink_with_no_surfers(self):
        """
        tests the roboflow_sink callback when no surfers are detected
        """
        #mock result with no surfer detections
        mock_result = {
            'predictions': [
                (0, 0, 100, 100, 0.9, {'class_name': 'Bird'}),
                {'class': 'Wave', 'confidence': 0.7}
            ]
        }
        
        #process the result
        self.analyzer.roboflow_sink(mock_result, None)
        
        #verify no surfers were counted
        self.assertEqual(self.analyzer.latest_result['surfer_count'], 0)
        self.assertEqual(self.analyzer.latest_result['status'], 'online')
    
    def test_roboflow_sink_with_invalid_data(self):
        """
        tests the roboflow_sink callback with invalid or malformed data.
        """
        #test with invalid data structure
        invalid_result = "invalid_data"
        
        #process the invalid result
        self.analyzer.roboflow_sink(invalid_result, None)
        
        #verify system handled the error gracefully
        self.assertEqual(self.analyzer.latest_result['surfer_count'], 0)
    
    def test_check_ffmpeg_process_running(self):
        """
        tests FFmpeg process health check when process is running.
        """
        #mock a running process
        mock_process = Mock()
        mock_process.poll.return_value = None  # None means process is running
        self.analyzer.ffmpeg_process = mock_process
        
        #check process health
        self.analyzer.check_ffmpeg_process()
        
        #process should not be terminated
        mock_process.terminate.assert_not_called()
    
    @patch.object(LiveStreamAnalyzer, 'start_ffmpeg_conversion')
    def test_check_ffmpeg_process_dead(self, mock_start_ffmpeg):
        """
        tests FFmpeg process health check when process has died.
        """
        #mock a dead process
        mock_process = Mock()
        mock_process.poll.return_value = 1  # Non-None means process is dead
        self.analyzer.ffmpeg_process = mock_process
        
        #mock successful restart
        mock_start_ffmpeg.return_value = True
        
        #check process health
        self.analyzer.check_ffmpeg_process()
        
        #process should be terminated and restarted
        mock_process.terminate.assert_called_once()
        mock_start_ffmpeg.assert_called_once()
    
    def test_stop_analysis(self):
        """
        tests clean shutdown of the analysis pipeline.
        """
        #mock active pipeline and process
        mock_pipeline = Mock()
        mock_process = Mock()
        self.analyzer.pipeline = mock_pipeline
        self.analyzer.ffmpeg_process = mock_process
        
        #stop analysis
        self.analyzer.stop_analysis()
        
        #verify cleanup
        mock_pipeline.terminate.assert_called_once()
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once()


class TestVideoAnalysisRoutes(unittest.TestCase):
    """
    tests for video analysis API routes
    """
    
    def setUp(self):
        """
        creates a test Flask app and clears global state.
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        #clear global state
        analysis_results.clear()
        active_pipelines.clear()
    
    def tearDown(self):
        """
        cleans up after each test method
        """
        self.app_context.pop()
    
    def test_get_video_analysis_no_webcam_id(self):
        """
        tests video analysis endpoint when no webcam_id is provided.
        """
        response = self.client.get('/api/video-analysis')
        self.assertEqual(response.status_code, 400)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No Webcam Selected')
    
    def test_get_video_analysis_invalid_webcam_id(self):
        """
        tests video analysis endpoint with invalid webcam_id.
        """
        response = self.client.get('/api/video-analysis?webcam_id=invalid_webcam')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'Webcam Not Available')
    
    @patch('routes.video_analysis.LiveStreamAnalyzer')
    def test_get_video_analysis_start_new_analysis(self, mock_analyzer_class):
        """
        tests starting a new video analysis for a valid webcam.
        """
        #mock analyzer instance
        mock_analyzer = Mock()
        mock_analyzer_class.return_value = mock_analyzer
        
        #use a valid webcam ID from config
        webcam_id = list(WEBCAM_CONFIGS.keys())[0]
        
        response = self.client.get(f'/api/video-analysis?webcam_id={webcam_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['webcam_id'], webcam_id)
        self.assertEqual(data['status'], 'Starting')
        self.assertEqual(data['surfer_count'], 0)
        self.assertIn('message', data)
        
        #verify analyzer was created and started
        mock_analyzer_class.assert_called_once()
        mock_analyzer.start_analysis.assert_called_once()
      
    def test_stop_analysis_existing_pipeline(self):
        """
        tests stopping an existing video analysis pipeline.
        """
        #set up existing pipeline
        webcam_id = "test_webcam"
        mock_analyzer = Mock()
        active_pipelines[webcam_id] = mock_analyzer
        analysis_results[webcam_id] = {'surfer_count': 1, 'status': 'online'}
        
        response = self.client.get(f'/api/stop-analysis/{webcam_id}')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        
        #verify cleanup
        mock_analyzer.stop_analysis.assert_called_once()
        self.assertNotIn(webcam_id, active_pipelines)
        self.assertNotIn(webcam_id, analysis_results)
    
    def test_stop_analysis_no_active_pipeline(self):
        """
        tests stopping analysis when no active pipeline exists.
        """
        response = self.client.get('/api/stop-analysis/nonexistent_webcam')
        self.assertEqual(response.status_code, 404)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertEqual(data['error'], 'No Active Analysis Found')
    
    def test_video_feed_no_active_pipeline(self):
        """
        tests video feed endpoint when no active pipeline exists.
        """
        response = self.client.get('/video_feed/nonexistent_webcam')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.data.decode(), 'Webcam not active')


class TestSurfDataRoutes(unittest.TestCase):
    """
    tests for surf data API routes.
    """
    
    def setUp(self):
        """
        sets up test fixtures before each test method.
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """
        cleans up after each test method.
        """
        self.app_context.pop()
    
    @patch('xarray.open_dataset')
    def test_get_surf_data_success(self, mock_open_dataset):
        """
        tests successful retrieval of surf data from CDIP buoys.
        """
        #mock dataset with valid wave data
        mock_dataset = Mock()
        mock_dataset.isel.return_value = mock_dataset
        mock_dataset.where.return_value = mock_dataset
        mock_dataset.waveTime.size = 10
        
        #mock wave data arrays
        mock_times = ['2023-01-01T12:00:00'] * 10
        mock_dataset.__getitem__.side_effect = lambda key: Mock(values=([1.5] * 10 if 'Hs' in key else [10.0] * 10))
        mock_dataset['waveTime'].values = mock_times
        
        mock_open_dataset.return_value = mock_dataset
        
        response = self.client.get('/api/surfdata?buoy_id=273')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('time', data)
        self.assertIn('waveHs', data)
        self.assertIn('waveTp', data)
        self.assertIn('waveDp', data)
        self.assertIn('waveTa', data)
        self.assertIn('waveTz', data)
        self.assertIn('wavePeakPSD', data)
    
    @patch('xarray.open_dataset')
    def test_get_surf_data_network_error(self, mock_open_dataset):
        """
        tests surf data endpoint when network/connection errors occur.
        """
        #mock network error
        mock_open_dataset.side_effect = Exception("Network error")
        
        response = self.client.get('/api/surfdata?buoy_id=273')
        self.assertEqual(response.status_code, 500)
        
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    def test_get_surf_data_default_buoy(self):
        """
        tests surf data endpoint with default buoy ID.
        """
        with patch('xarray.open_dataset') as mock_open_dataset:
            #mock successful dataset
            mock_dataset = Mock()
            mock_dataset.isel.return_value = mock_dataset
            mock_dataset.where.return_value = mock_dataset
            mock_dataset.waveTime.size = 10
            mock_open_dataset.return_value = mock_dataset
            
            response = self.client.get('/api/surfdata')
            #should use default buoy_id without errors
            mock_open_dataset.assert_called_once()
            call_args = mock_open_dataset.call_args[0][0]
            self.assertIn('273', call_args)  # Default buoy ID


class TestFrontendRoutes(unittest.TestCase):
    """
    tests for frontend serving routes.
    """
    
    def setUp(self):
        """
        aets up test fixtures before each test method.
        """
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """
        cleans up after each test method.
        """
        self.app_context.pop()
    
    @patch('routes.frontend.render_template')
    def test_serve_frontend(self, mock_render_template):
        """
        tests that the frontend route serves the main application page.
        """
        mock_render_template.return_value = "<html>Frontend</html>"
        
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
        mock_render_template.assert_called_once_with('frontend.html')


class TestAppCreation(unittest.TestCase):
    """
    tests for Flask application creation and configuration.
    """
    
    def test_create_app_returns_flask_instance(self):
        """
        tests that create_app returns a proper Flask application instance
        """
        app = create_app()
        self.assertIsNotNone(app)
        self.assertEqual(app.__class__.__name__, 'Flask')
    
    def test_app_has_required_blueprints(self):
        """
        tests that the application has all required blueprints registered
        """
        app = create_app()
        
        #check that blueprints are registered
        blueprint_names = [bp.name for bp in app.blueprints.values()]
        self.assertIn('video_analysis', blueprint_names)
        self.assertIn('surf_data', blueprint_names)
        self.assertIn('frontend', blueprint_names)
    
    def test_app_config_loaded(self):
        """
        tests that the application configuration is properly loaded
        """
        app = create_app()
        
        #check that config is loaded from Config class
        self.assertEqual(app.config['DEBUG'], Config.DEBUG)
        self.assertEqual(app.config['MAX_FPS'], Config.MAX_FPS)


if __name__ == '__main__':
    unittest.main()
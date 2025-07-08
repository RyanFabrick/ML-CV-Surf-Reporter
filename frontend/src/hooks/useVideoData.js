import { useState, useEffect } from 'react';

//custom hook for fetching video analysis data from webcams
export const useVideoData = (selectedWebcam) => {
  //webcam specific state
  const [videoData, setVideoData] = useState(null);
  const [webcamError, setWebcamError] = useState(null);
  const [analysisStatus, setAnalysisStatus] = useState('');

  const fetchVideoData = (webcamId) => {
    if (!webcamId) {
      //no webcam selected, clear data
      setVideoData(null);
      setWebcamError(null);
      setAnalysisStatus('');
      return;
    }
    
    fetch(`http://localhost:5000/api/video-analysis?webcam_id=${webcamId}`)
      .then((res) => res.json())
      .then((json) => {
        if (json.error) {
          setWebcamError(`Webcam Error: ${json.error}`);
          setVideoData(null);
          setAnalysisStatus('error');
        } else {
          setVideoData(json);
          setWebcamError(null);
          setAnalysisStatus(json.status);

          //Show status messages
          if (json.status === 'starting') {
            setAnalysisStatus('Starting Analysis...');
          } else if (json.status === 'initializing') {
            setAnalysisStatus('Initializing Analysis...');
          } else if (json.status === 'online') {
            setAnalysisStatus('Live'); 
          } else if (json.status === 'error') {
            setAnalysisStatus('Analysis Error');
          }
        }
      })
      .catch((err) => {
        console.error('Webcam Data Fetch Error:', err);
        setWebcamError('Failed to fetch webcam data');
        setVideoData(null);
        setAnalysisStatus('error');
      });
  };

  useEffect(() => {
    //initial data fetch
    fetchVideoData(selectedWebcam);

    const videoInterval = setInterval(() => {
      if (selectedWebcam) {
        fetchVideoData(selectedWebcam);
      }
    }, 5000); // 5 seconds
    
    return () => {
      clearInterval(videoInterval);
    };
  }, [selectedWebcam]); // rerun when selection changes

  return { videoData, webcamError, analysisStatus, fetchVideoData };
};
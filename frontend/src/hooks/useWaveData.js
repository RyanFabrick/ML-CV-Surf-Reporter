import { useState, useEffect } from 'react';

//custom hook for fetching wave data from buoys
export const useWaveData = (selectedBuoy) => {
  //data -> data from Flask backend
  const [data, setData] = useState(null);
  //error -> possible error during fetch
  const [error, setError] = useState(null);

  //runs after empty array is ran, after component mounts
  //fetches data from Flask endpoint
  //stores in data, if error stores error message
  const fetchWaveData = (buoyId) => {
    //does not fetch if no buoy selected
    if (!buoyId) {
      setData(null);
      setError(null);
      return;
    }

    fetch(`http://localhost:5000/api/surfdata?buoy_id=${buoyId}`)
      .then((res) => res.json())
      .then((json) => {
        if (json.error) {
          setError(`Buoy Data Error: ${json.error}`);
          setData(null);
        } else {
          setData(json);
          setError(null);
        }
      })
      .catch((err) => {
        console.error('Wave Data Fetch Error:', err);
        setError('Failed to fetch wave data - check connection');
        setData(null);
      });
  };

  useEffect(() => {
    //initial data fetch
    fetchWaveData(selectedBuoy);

    const waveInterval = setInterval(() => {
      fetchWaveData(selectedBuoy);
    }, 180000); // 3 minutes
    
    return () => {
      clearInterval(waveInterval);
    };
  }, [selectedBuoy]); // rerun when selection changes

  return { data, error, fetchWaveData };
};
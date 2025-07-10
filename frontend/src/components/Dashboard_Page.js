import React from 'react';
import VideoPanel from './Video_Panel';
import WaveDataPanel from './Wave_Data_Panel';
import ChartPanel from './Chart_Panel';
import HistoricalDataPanel from './Historical_Data_Panel';

const DashboardPage = ({ 
  selectedBuoy, 
  selectedWebcam, 
  data, 
  error, 
  videoData, 
  webcamError, 
  analysisStatus,
  onNavigate
}) => (
  <div className="dashboard">

    <VideoPanel 
      selectedWebcam={selectedWebcam}
      videoData={videoData}
      webcamError={webcamError}
      analysisStatus={analysisStatus}
      onNavigate={onNavigate}
    />

    <WaveDataPanel 
      selectedBuoy={selectedBuoy}
      data={data}
    />

    <ChartPanel 
      selectedBuoy={selectedBuoy}
      data={data}
      error={error}
    />

    <HistoricalDataPanel 
      selectedBuoy={selectedBuoy}
      data={data}
      error={error}
      onNavigate={onNavigate}
    />
  </div>
  
);

export default DashboardPage;
import React from 'react';
import VideoPanel from './Video_Panel';
import WaveDataPanel from './Wave_Data_Panel';
import ChartPanel from './Chart_Panel';
import HistoricalDataPanel from './Historical_Data_Panel';

// Main Dashboard Component
const DashboardPage = ({ 
  selectedBuoy, 
  selectedWebcam, 
  data, 
  error, 
  videoData, 
  webcamError, 
  analysisStatus 
}) => (
  <div className="dashboard">
    {/* Video Analysis Panel */}
    <VideoPanel 
      selectedWebcam={selectedWebcam}
      videoData={videoData}
      webcamError={webcamError}
      analysisStatus={analysisStatus}
    />

    {/* Current Wave Data Panel */}
    <WaveDataPanel 
      selectedBuoy={selectedBuoy}
      data={data}
    />

    {/* Chart Panel */}
    <ChartPanel 
      selectedBuoy={selectedBuoy}
      data={data}
      error={error}
    />

    {/* Historical Data Panel */}
    <HistoricalDataPanel 
      selectedBuoy={selectedBuoy}
      data={data}
      error={error}
    />
  </div>
);

export default DashboardPage;
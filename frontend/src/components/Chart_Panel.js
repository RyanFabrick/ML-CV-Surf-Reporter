import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { prepareChartData } from '../utils/prepareChartData';

const ChartPanel = ({ selectedBuoy, data, error }) => {
  //prepares data for Recharts
  //transforms raw API data into readable Recharts data
  const chartData = data ? prepareChartData(data) : [];

  return (
    <div className="panel chart-panel">
      <div className="panel-header">
        <h2 className="panel-title">Wave Height Timeline</h2>
      </div>
      <div className="chart-container">
        {!selectedBuoy ? (
          <div className="loading">Select a buoy to view wave data chart</div>
        ) : error ? (
          <div className="error">Error: {error}</div>
        ) : !data ? (
          <div className="loading">Loading chart data...</div>
        ) : (
          /* ResponsiveContainer makes the chart resize with the window */
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              {/* CartesianGrid adds the background grid lines */}
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
              {/* XAxis shows the time labels at bottom */}
              <XAxis 
                dataKey="time" 
                stroke="#a0a0a0"
                fontSize={12}
              />
              {/* YAxis shows the wave height values on left */}
              <YAxis 
                stroke="#a0a0a0"
                fontSize={12}
              />
              {/* Tooltip shows details when you hover over points */}
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#1a1a1a',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                  color: '#ffffff'
                }}
              />
              {/* Legend explains what the lines represent */}
              <Legend />
              {/* The actual line that shows wave height data */}
              <Line 
                type="monotone"           // Smooth curved line
                dataKey="waveHeight"     // Which data to plot (from chartData)
                stroke="#00d4ff"         // Line color (your blue theme)
                strokeWidth={2}          // Line thickness
                name="Wave Height (m)"   // Label in legend and tooltip
                dot={{ fill: '#00d4ff', strokeWidth: 2, r: 4 }}
                activeDot={{ r: 6, fill: '#00d4ff' }}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
      </div>
    </div>
  );
};

export default ChartPanel;
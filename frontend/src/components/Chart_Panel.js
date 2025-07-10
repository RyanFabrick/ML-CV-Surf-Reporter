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
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255, 255, 255, 0.1)" />
              <XAxis 
                dataKey="time" 
                stroke="#a0a0a0"
                fontSize={12}
              />
              <YAxis 
                stroke="#a0a0a0"
                fontSize={12}
              />
              <Tooltip 
                contentStyle={{
                  backgroundColor: '#1a1a1a',
                  border: '1px solid rgba(255, 255, 255, 0.1)',
                  borderRadius: '8px',
                  color: '#ffffff'
                }}
              />
              <Legend />
              <Line 
                type="monotone"           //smooth curved line
                dataKey="waveHeight"     //which data to plot
                stroke="#00d4ff"         //line color
                strokeWidth={2}          //line thickness
                name="Wave Height (m)"   //label in legend and tooltip
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
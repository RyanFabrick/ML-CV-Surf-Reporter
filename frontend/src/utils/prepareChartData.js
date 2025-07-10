//prepares data for Recharts
//transforms raw API data into readable Recharts data
export function prepareChartData(apiData) {
  //creates array of chart points - combines time and wave measurements
  const ChartPoints = apiData.time.map((timeString, index) => {
    //converts to date object
    const dateObj = new Date(timeString);
    //formats to 12 hr time with am/pm
    const timeOnly = dateObj.toLocaleTimeString([], {
      hour: 'numeric',
      minute: '2-digit',
      hour12: true
    });
    //creates a data point object from moment in time
    return {
      time: timeOnly, //x-axis
      waveHeight: apiData.waveHs[index], //y-axis
      peakPeriod: apiData.waveTp[index] //y-axis
    };
  });
  //reverse array - older measurements on left side
  return ChartPoints;
}

export function extractTimeFromString(timeString) {
  //splits spaces, takes time, original if no spaces
  return timeString.split(' ')[1] || timeString;
}
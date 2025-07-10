//function to get current wave data from latest measurements
export const getCurrentWaveData = (data) => {
  if (!data || !data.waveHs || data.waveHs.length === 0) {
    return {
      waveHeight: '--',
      peakPeriod: '--',
      waveDirection: '--',
      avgPeriod: '--'
    };
  }
  
  const latest = data.waveHs.length - 1;
  return {
    waveHeight: data.waveHs[latest]?.toFixed(1) || '--',
    peakPeriod: data.waveTp[latest]?.toFixed(1) || '--',
    waveDirection: data.waveDp[latest]?.toFixed(0) || '--',
    avgPeriod: data.waveTa[latest]?.toFixed(1) || '--'
  };
};
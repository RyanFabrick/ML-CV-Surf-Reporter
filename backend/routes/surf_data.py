import xarray as xr #for multi dimesional arrays, helpful for NetCDF files
import pandas as pd #data manipulation/analysis (needed for datetime conversion format)
from flask import Blueprint, jsonify, request

surf_data_bp = Blueprint('surf_data', __name__)

@surf_data_bp.route('/api/surfdata')

def get_surf_data():
    """
    api endpoint to retrieve wave data from CDIP buoys
    accepts buoy_id param for query
    connects to CDIP THREDDS server to access NetCDF
    fileters for 'good' data points
    extracts paramters wanted
    formats timestamps for frontend display

    returns JSON data for frontend retreival
    returns wave height, peak wave peirod, wave direction, average wave period
    mean zero upcrossing period, and peak power spectral density
    """
    #gets buoy_id from query parameters, default - 237
    buoy_id = request.args.get('buoy_id', '273')
    
    try:    
        #url for cdip real-time data
        #gives oPeNDAP access to netcdf files
        url = f'https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/{buoy_id}p1_rt.nc'

        #opens dataset remotely vis opendap
        #xarray handles network connection, data parsing
        ds = xr.open_dataset(url)

        ds = ds.isel(waveTime=slice(-30, None))

        #CDIP documentation reccomenndation
        #keeps only "good" records
        # 1 - good, 2 - not evaluated, 3 - questionable, 4 - bad
        good = ds['waveFlagPrimary'] == 1
        #removes flagged data and checks
        ds = ds.where(good, drop=True)
        if ds.waveTime.size == 0:
            return jsonify({'error': 'No Valid Wave Data Found'}), 404
        
        #timestamps
        times = ds['waveTime'].values[:10]
        # wave height significant (waveHs),
        wave_height_significant = ds['waveHs'].values[:10]
        # peak wave period (waveTp),
        wave_tp = ds['waveTp'].values[:10]
        # peak wave direction (waveDp)
        wave_dp = ds['waveDp'].values[:10]
        # avg wave period (waveTa),
        wave_ta = ds['waveTa'].values[:10]
        # mean zero-upcrossing period (waveTz),
        wave_tz = ds['waveTz'].values[:10]
        # peak wave power spectral density (wavePeakPSD)
        wave_psd = ds['wavePeakPSD'].values[:10]

        #numpy.datetime64 to readable
        readable_time = []
        for t in times:
            #converts to pandas.Timestamp
            timestamp = pd.to_datetime(t)
            #formats as 'YYY-MM-DD HH:MM'
            formatted = timestamp.strftime('%Y-%m-%d %I:%M %p')
            #appends to list
            readable_time.append(formatted)

        #returns structured JSON
        #numpy arrays converted to lists
        return jsonify({

            'time': readable_time,
            "waveHs": wave_height_significant.tolist(),
            "waveTp": wave_tp.tolist(),
            "waveDp": wave_dp.tolist(),
            "waveTa": wave_ta.tolist(),
            "waveTz": wave_tz.tolist(),
            "wavePeakPSD": wave_psd.tolist()

        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
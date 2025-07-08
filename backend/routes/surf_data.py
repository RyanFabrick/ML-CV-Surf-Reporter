import xarray as xr
import pandas as pd
from flask import Blueprint, jsonify, request

surf_data_bp = Blueprint('surf_data', __name__)

#Exisitng surfdata route accepts bupy_id parameter
@surf_data_bp.route('/api/surfdata')
def get_surf_data():
    
    #gets buoy_id from query parameters, default - 237(point dume)
    buoy_id = request.args.get('buoy_id', '273')
    
    try:    
        # Step 1: ppoint to public netCDF file for data 
        # (Point Dume Bouy - 273)
        url = f'https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/{buoy_id}p1_rt.nc'

        # checks connectivity to CDIP server
        #try:
        #    urllib.request.urlopen(url, timeout=30)
        #except Exception as e:
        #    return jsonify({'error': 'CDIP Server Unreachable', 'Details': str(e)}), 504

        # loads .nc file directly
        #ds = xr.open_dataset('273p1_rt.nc')

        # opens dataset remotely
        ds = xr.open_dataset(url)

        ds = ds.isel(waveTime=slice(-30, None))

        # Step 2: filter for "good" records
        # CDIP documentation reccomenndation
        # keeps only "good" records
        good = ds['waveFlagPrimary'] == 1
        ds = ds.where(good, drop=True)
        if ds.waveTime.size == 0:
            return jsonify({'error': 'No Valid Wave Data Found'}), 404

        # Step 3: Extract relevant data
        # Relevant data: time, 
        # wave height significant (waveHs),
        # peak wave period (waveTp),
        # peak wave direction (waveDp),
        # avg wave period (waveTa),
        # mean zero-upcrossing period (waveTz),
        # peak wave power spectral density (wavePeakPSD)
        times = ds['waveTime'].values[:10]
        wave_height_significant = ds['waveHs'].values[:10]
        wave_tp = ds['waveTp'].values[:10]
        wave_dp = ds['waveDp'].values[:10]
        wave_ta = ds['waveTa'].values[:10]
        wave_tz = ds['waveTz'].values[:10]
        wave_psd = ds['wavePeakPSD'].values[:10]

        # Step 4: convert UNIX to readable format
        #converts numpy.datetime64 to Python datetime/format, each
        readable_time = []
        for t in times:
            #converts to pandas.Timestamp
            timestamp = pd.to_datetime(t)
            #formats as 'YYY-MM-DD HH:MM'
            formatted = timestamp.strftime('%Y-%m-%d %I:%M %p')
            #appends to list
            readable_time.append(formatted)

        # Step 5: returns data to frontend as JSON
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
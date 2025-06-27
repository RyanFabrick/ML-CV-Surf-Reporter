import xarray as xr
import urllib.request

from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file
from flask import render_template
#CORS allows cross-origin requests
#useful for frontend-backend communication
from flask_cors import CORS
from datetime import datetime, timezone

app = Flask(__name__)
CORS(app)

@app.route('/')
def serve_frontend():

    return render_template('frontend.html')

#main shit
@app.route('/api/surfdata')
def get_surf_data():
    try:    
        # Step 1: ppoint to public netCDF file for data 
        # (Point Dume Bouy - 273)
        url= 'https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/273p1_rt.nc'

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

        # slices first 10 elements of 'times',
        # converts (t) to string,
        # stores in readable_time
        readable_time = [str(t) for t in times]

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


if __name__ == '__main__':
    app.run(debug = True)
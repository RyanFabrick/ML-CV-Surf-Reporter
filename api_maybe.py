import xarray as xr

from flask import Flask
from flask import jsonify
from flask import request
from flask import send_file
from flask import render_template
from datetime import datetime, timezone

app = Flask(__name__)

@app.route('/')
def serve_frontend():

    return render_template('frontend.html')

#main shit
@app.route('/api/surfdata')
def get_surf_data():
    try:    
        # Step 1: ppoint to public netCDF file for data 
        # (Dana Point Buoy - station 093)
        url= 'https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/rt_093.nc'
        
        # loads .nc file directly
        ds = xr.open_dataset('273p1_rt.nc')

        # Step 2: filter for "good" records
        # CDIP documentation reccomenndation
        good = ds['waveFlagPrimary'] == 1

        # Step 3: Extract relevant data
        # Relevant data: time, 
        # wave height significant (waveHs),
        # peak wave period (waveTp),
        # peak wave direction (waveDp),
        # avg wave period (waveTa),
        # mean zero-upcrossing period (waveTz),
        # peak wave power spectral density (wavePeakPSD)
        times = ds['waveTime'].values[good]
        wave_height_signficant = ds['waveHs'].values[good]
        wave_tp = ds['waveTp'].values[good]
        wave_dp = ds['waveDp'].values[good]
        wave_ta = ds['waveTa'].values[good]
        wave_tz = ds['waveTz'].values[good]
        wave_psd = ds['wavePeakPSD'].values[good]

        # Step 4: convert UNIX to readable format

        # slices first 10 elements of 'times',
        # loops for first 10 elements, 
        # converts (t) to string,
        # stores in readable_time
        readable_time = [str(t) for t in times[:10]]

        # Step 5: returns data to frontend as JSON
        return jsonify({

            'time': readable_time,
            "waveHs": wave_height_signficant[:10].tolist(),
            "waveTp": wave_tp[:10].tolist(),
            "waveDp": wave_dp[:10].tolist(),
            "waveTa": wave_ta[:10].tolist(),
            "waveTz": wave_tz[:10].tolist(),
            "wavePeakPSD": wave_psd[:10].tolist()

        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug = True)
from flask import Blueprint, jsonify, request
import xarray as xr
import pandas as pd

surf_data_blueprint = Blueprint('surf_data', __name__)

@surf_data_blueprint.route('/data', methods=['GET'])
def get_surf_data():
    buoy_id = request.args.get('buoy_id', '273')
    url = f'https://thredds.cdip.ucsd.edu/thredds/dodsC/cdip/realtime/{buoy_id}p1_rt.nc'
    try:
        ds = xr.open_dataset(url)
        ds = ds.isel(waveTime=slice(-30, None))
        ds = ds.where(ds['waveFlagPrimary'] == 1, drop=True)
        if ds.waveTime.size == 0:
            return jsonify({'error': 'No valid wave data found'}), 404

        times = pd.to_datetime(ds['waveTime'].values[:10])
        readable_time = [t.strftime('%Y-%m-%d %I:%M %p') for t in times]

        return jsonify({
            'time': readable_time,
            'waveHs': ds['waveHs'].values[:10].tolist(),
            'waveTp': ds['waveTp'].values[:10].tolist(),
            'waveDp': ds['waveDp'].values[:10].tolist(),
            'waveTa': ds['waveTa'].values[:10].tolist(),
            'waveTz': ds['waveTz'].values[:10].tolist(),
            'wavePeakPSD': ds['wavePeakPSD'].values[:10].tolist()
        })
    except Exception as e:
        print(f"Surf data error: {e}")
        return jsonify({'error': str(e)}), 500

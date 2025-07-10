from flask import Flask #core framwork for web appliications
from flask_cors import CORS #handles cross origin resource sharing for api acesss
                            #frontend on diff port/domains to get backend apis
from routes.video_analysis import video_analysis_bp #handles surfer detection
from routes.surf_data import surf_data_bp #handles surf conditons
from routes.frontend import frontend_bp #serves main frotned
from config import Config #app settings and constants

def create_app():
    """
    congigures creates Flask application
    returns flask app instance ready to runnnn
    """
    #creates instance
    app = Flask(__name__)
    #enables CORS
    CORS(app)
    
    #loads configuration
    app.config.from_object(Config)
    
    #register blueprints
    app.register_blueprint(video_analysis_bp)
    app.register_blueprint(surf_data_bp)
    app.register_blueprint(frontend_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
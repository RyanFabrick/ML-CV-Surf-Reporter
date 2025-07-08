from flask import Flask
from flask_cors import CORS
from backend.routes.api import api_blueprint
from backend.routes.video import video_blueprint
from backend.config import Config

def create_app():
    app = Flask(__name__)
    
    # Load config
    app.config.from_object(Config)
    
    # Enable CORS
    CORS(app)

    # Register Blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')
    app.register_blueprint(video_blueprint, url_prefix='/api/video')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
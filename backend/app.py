from flask import Flask
from flask_cors import CORS
from routes.video_analysis import video_analysis_bp
from routes.surf_data import surf_data_bp
from routes.frontend import frontend_bp
from config import Config

def create_app():
    """Factory function to create Flask application"""
    app = Flask(__name__)
    CORS(app)
    
    # Load configuration
    app.config.from_object(Config)
    
    # Register blueprints
    app.register_blueprint(video_analysis_bp)
    app.register_blueprint(surf_data_bp)
    app.register_blueprint(frontend_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
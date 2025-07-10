from flask import Blueprint, render_template #organziation of routes

#creates blueprint for frontend routes
#with main flask app
frontend_bp = Blueprint('frontend', __name__)

@frontend_bp.route('/')
def serve_frontend():
    return render_template('frontend.html')
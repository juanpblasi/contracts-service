"""
Flask Application Entry Point
Contract Comparison Service
"""
import os
import logging
from flask import Flask
from flask_cors import CORS

from config import get_config
from api.routes import api_bp
from utils.helpers import ensure_directory_exists

# Get configuration
config = get_config()

# Configure logging
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format=config.LOG_FORMAT
)
logger = logging.getLogger(__name__)


def create_app(config_name=None):
    """
    Application factory pattern
    
    Args:
        config_name: Configuration name (development, production, etc.)
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(get_config(config_name))
    
    # Enable CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": config.CORS_ORIGINS,
            "methods": ["GET", "POST", "OPTIONS"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Ensure upload directory exists
    ensure_directory_exists(config.UPLOAD_FOLDER)
    
    # Register blueprints
    app.register_blueprint(api_bp, url_prefix=config.API_PREFIX)
    
    # Root endpoint
    @app.route('/')
    def index():
        return {
            'service': 'Contract Comparison Service',
            'version': '1.0.0',
            'status': 'running',
            'endpoints': {
                'health': f'{config.API_PREFIX}/health',
                'compare': f'{config.API_PREFIX}/compare',
                'compare_html': f'{config.API_PREFIX}/compare/html'
            }
        }
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'status': 'error', 'message': 'Resource not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f'Internal server error: {error}')
        return {'status': 'error', 'message': 'Internal server error'}, 500
    
    logger.info('Contract Comparison Service initialized')
    
    return app


if __name__ == '__main__':
    # Create and run the application
    app = create_app()
    
    # Run server
    port = int(os.environ.get('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=config.DEBUG
    )

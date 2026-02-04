"""
Vercel Serverless Function Entry Point
"""
import sys
from pathlib import Path

# Add backend directory to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

from app import create_app

# Create Flask app instance for Vercel
app = create_app('production')

# Vercel handler
def handler(request, response):
    return app(request, response)

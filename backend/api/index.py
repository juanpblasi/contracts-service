"""
Vercel Serverless Function Entry Point
"""
from app import create_app

# Create Flask app instance for Vercel
app = create_app('production')

# Export the app for Vercel
# Vercel will call this as a serverless function
handler = app

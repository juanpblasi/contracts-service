"""
Helper utility functions
"""
import os
import uuid
from datetime import datetime
from pathlib import Path


def generate_unique_filename(original_filename):
    """
    Generate a unique filename while preserving extension
    
    Args:
        original_filename: Original name of the file
        
    Returns:
        str: Unique filename with timestamp and UUID
    """
    name, ext = os.path.splitext(original_filename)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    unique_id = str(uuid.uuid4())[:8]
    return f"{name}_{timestamp}_{unique_id}{ext}"


def cleanup_temp_files(directory, max_age_hours=24):
    """
    Remove temporary files older than specified age
    
    Args:
        directory: Directory path to clean
        max_age_hours: Maximum age in hours (default: 24)
    """
    if not os.path.exists(directory):
        return
    
    now = datetime.now().timestamp()
    max_age_seconds = max_age_hours * 3600
    
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_age = now - os.path.getmtime(filepath)
            if file_age > max_age_seconds:
                try:
                    os.remove(filepath)
                except Exception as e:
                    print(f"Error removing {filepath}: {e}")


def ensure_directory_exists(directory):
    """
    Ensure a directory exists, create if it doesn't
    
    Args:
        directory: Directory path to check/create
    """
    Path(directory).mkdir(parents=True, exist_ok=True)


def format_percentage(value, total):
    """
    Format a value as a percentage of total
    
    Args:
        value: The value
        total: The total
        
    Returns:
        float: Percentage rounded to 2 decimal places
    """
    if total == 0:
        return 0.0
    return round((value / total) * 100, 2)

"""
File validation utilities
"""
import os
from werkzeug.utils import secure_filename
from config import Config


def allowed_file(filename):
    """
    Check if file extension is allowed
    
    Args:
        filename: Name of the file to check
        
    Returns:
        bool: True if file extension is allowed, False otherwise
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS


def validate_file_size(file_obj, max_size=None):
    """
    Validate file size doesn't exceed maximum
    
    Args:
        file_obj: File object to check
        max_size: Maximum size in bytes (defaults to Config.MAX_FILE_SIZE)
        
    Returns:
        tuple: (is_valid, error_message)
    """
    if max_size is None:
        max_size = Config.MAX_FILE_SIZE
    
    # Get current position
    current_position = file_obj.tell()
    
    # Seek to end to get file size
    file_obj.seek(0, os.SEEK_END)
    file_size = file_obj.tell()
    
    # Reset to original position
    file_obj.seek(current_position)
    
    if file_size > max_size:
        max_mb = max_size / (1024 * 1024)
        return False, f"File size exceeds maximum allowed ({max_mb:.1f} MB)"
    
    return True, None


def validate_upload(file_obj):
    """
    Comprehensive validation for uploaded files
    
    Args:
        file_obj: FileStorage object from Flask request
        
    Returns:
        tuple: (is_valid, error_message, secure_name)
    """
    if not file_obj or file_obj.filename == '':
        return False, "No file provided", None
    
    filename = file_obj.filename
    
    # Check file extension
    if not allowed_file(filename):
        allowed_exts = ', '.join(Config.ALLOWED_EXTENSIONS)
        return False, f"File type not allowed. Allowed types: {allowed_exts}", None
    
    # Check file size
    is_valid_size, size_error = validate_file_size(file_obj)
    if not is_valid_size:
        return False, size_error, None
    
    # Generate secure filename
    secure_name = secure_filename(filename)
    
    return True, None, secure_name

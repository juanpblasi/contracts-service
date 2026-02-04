"""
API Routes for Contract Comparison Service
"""
import os
from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename

from services.file_parser import FileParser
from services.comparator import ContractComparator
from services.report_generator import ReportGenerator
from utils.validators import validate_upload
from utils.helpers import generate_unique_filename, ensure_directory_exists
from config import get_config

# Create blueprint
api_bp = Blueprint('api', __name__)

# Get configuration
config = get_config()

# Ensure upload directory exists
ensure_directory_exists(config.UPLOAD_FOLDER)


@api_bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint
    
    Returns:
        JSON response with service status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'Contract Comparison Service',
        'version': '1.0.0'
    }), 200


@api_bp.route('/compare', methods=['POST'])
def compare_contracts():
    """
    Compare two contract files
    
    Expected request:
        - multipart/form-data
        - file1: First contract file
        - file2: Second contract file
    
    Returns:
        JSON response with comparison report
    """
    try:
        # Check if files are in request
        if 'file1' not in request.files or 'file2' not in request.files:
            return jsonify({
                'status': 'error',
                'message': 'Both file1 and file2 are required'
            }), 400
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # Validate file1
        is_valid1, error1, secure_name1 = validate_upload(file1)
        if not is_valid1:
            return jsonify({
                'status': 'error',
                'message': f'File 1 validation failed: {error1}'
            }), 400
        
        # Validate file2
        is_valid2, error2, secure_name2 = validate_upload(file2)
        if not is_valid2:
            return jsonify({
                'status': 'error',
                'message': f'File 2 validation failed: {error2}'
            }), 400
        
        # Save files temporarily
        filename1 = generate_unique_filename(secure_name1)
        filename2 = generate_unique_filename(secure_name2)
        
        filepath1 = os.path.join(config.UPLOAD_FOLDER, filename1)
        filepath2 = os.path.join(config.UPLOAD_FOLDER, filename2)
        
        file1.save(filepath1)
        file2.save(filepath2)
        
        try:
            # Parse files
            parser = FileParser()
            data1 = parser.parse_file(filepath1)
            data2 = parser.parse_file(filepath2)
            
            # Normalize data
            data1 = parser.normalize_data(data1)
            data2 = parser.normalize_data(data2)
            
            # Compare contracts
            comparator = ContractComparator()
            comparison_result = comparator.compare(data1, data2)
            
            # Generate report
            report_gen = ReportGenerator()
            report = report_gen.generate_json_report(
                comparison_result,
                secure_name1,
                secure_name2
            )
            
            return jsonify({
                'status': 'success',
                'report': report
            }), 200
            
        finally:
            # Clean up temporary files
            try:
                if os.path.exists(filepath1):
                    os.remove(filepath1)
                if os.path.exists(filepath2):
                    os.remove(filepath2)
            except Exception as e:
                print(f"Error cleaning up files: {e}")
    
    except ValueError as e:
        return jsonify({
            'status': 'error',
            'message': f'File parsing error: {str(e)}'
        }), 400
    
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Internal server error: {str(e)}'
        }), 500


@api_bp.route('/compare/html', methods=['POST'])
def compare_contracts_html():
    """
    Compare two contract files and return HTML report
    
    Expected request:
        - multipart/form-data
        - file1: First contract file
        - file2: Second contract file
    
    Returns:
        HTML report
    """
    try:
        # Check if files are in request
        if 'file1' not in request.files or 'file2' not in request.files:
            return "Error: Both file1 and file2 are required", 400
        
        file1 = request.files['file1']
        file2 = request.files['file2']
        
        # Validate files
        is_valid1, error1, secure_name1 = validate_upload(file1)
        if not is_valid1:
            return f"File 1 validation failed: {error1}", 400
        
        is_valid2, error2, secure_name2 = validate_upload(file2)
        if not is_valid2:
            return f"File 2 validation failed: {error2}", 400
        
        # Save files temporarily
        filename1 = generate_unique_filename(secure_name1)
        filename2 = generate_unique_filename(secure_name2)
        
        filepath1 = os.path.join(config.UPLOAD_FOLDER, filename1)
        filepath2 = os.path.join(config.UPLOAD_FOLDER, filename2)
        
        file1.save(filepath1)
        file2.save(filepath2)
        
        try:
            # Parse files
            parser = FileParser()
            data1 = parser.parse_file(filepath1)
            data2 = parser.parse_file(filepath2)
            
            # Normalize data
            data1 = parser.normalize_data(data1)
            data2 = parser.normalize_data(data2)
            
            # Compare contracts
            comparator = ContractComparator()
            comparison_result = comparator.compare(data1, data2)
            
            # Generate HTML report
            report_gen = ReportGenerator()
            html_report = report_gen.generate_html_report(
                comparison_result,
                secure_name1,
                secure_name2
            )
            
            return html_report, 200, {'Content-Type': 'text/html; charset=utf-8'}
            
        finally:
            # Clean up temporary files
            try:
                if os.path.exists(filepath1):
                    os.remove(filepath1)
                if os.path.exists(filepath2):
                    os.remove(filepath2)
            except Exception as e:
                print(f"Error cleaning up files: {e}")
    
    except Exception as e:
        return f"Internal server error: {str(e)}", 500

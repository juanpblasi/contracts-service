"""
Tests for file parser module
"""
import pytest
import json
import os
import tempfile
from services.file_parser import FileParser


class TestFileParser:
    """Test cases for FileParser"""
    
    def test_detect_json_file_type(self):
        """Test JSON file type detection"""
        assert FileParser.detect_file_type('test.json') == 'json'
        assert FileParser.detect_file_type('/path/to/file.json') == 'json'
    
    def test_detect_csv_file_type(self):
        """Test CSV file type detection"""
        assert FileParser.detect_file_type('test.csv') == 'csv'
    
    def test_detect_excel_file_type(self):
        """Test Excel file type detection"""
        assert FileParser.detect_file_type('test.xlsx') == 'excel'
        assert FileParser.detect_file_type('test.xls') == 'excel'
    
    def test_parse_json(self):
        """Test JSON parsing"""
        # Create temporary JSON file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_data = {
                'name': 'John Doe',
                'age': 30,
                'city': 'New York'
            }
            json.dump(test_data, f)
            temp_path = f.name
        
        try:
            # Parse the file
            result = FileParser.parse_json(temp_path)
            
            # Assertions
            assert result['name'] == 'John Doe'
            assert result['age'] == 30
            assert result['city'] == 'New York'
        finally:
            # Cleanup
            os.unlink(temp_path)
    
    def test_normalize_data_converts_numbers(self):
        """Test data normalization converts string numbers"""
        data = {
            'string_int': '42',
            'string_float': '3.14',
            'real_string': 'hello',
            'nested': {
                'value': '100'
            }
        }
        
        normalized = FileParser.normalize_data(data)
        
        assert normalized['string_int'] == 42
        assert normalized['string_float'] == 3.14
        assert normalized['real_string'] == 'hello'
        assert normalized['nested']['value'] == 100
    
    def test_parse_file_invalid_type(self):
        """Test parsing unsupported file type"""
        with pytest.raises(ValueError):
            FileParser.parse_file('test.invalid')

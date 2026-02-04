"""
File parser module - Handles parsing of multiple file formats
"""
import json
import pandas as pd
from pathlib import Path


class FileParser:
    """Parser for contract files in various formats"""
    
    @staticmethod
    def detect_file_type(filepath):
        """
        Detect file type from extension
        
        Args:
            filepath: Path to the file
            
        Returns:
            str: File type ('json', 'csv', 'excel', 'pdf', 'unknown')
        """
        extension = Path(filepath).suffix.lower()
        
        if extension == '.json':
            return 'json'
        elif extension == '.csv':
            return 'csv'
        elif extension in ['.xlsx', '.xls']:
            return 'excel'
        elif extension == '.pdf':
            return 'pdf'
        elif extension == '.txt':
            return 'txt'
        else:
            return 'unknown'
    
    @staticmethod
    def parse_json(filepath):
        """
        Parse JSON file to dictionary
        
        Args:
            filepath: Path to JSON file
            
        Returns:
            dict: Parsed data
        """
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    
    @staticmethod
    def parse_csv(filepath):
        """
        Parse CSV file to dictionary
        
        Args:
            filepath: Path to CSV file
            
        Returns:
            dict: Parsed data (first row as dictionary)
        """
        df = pd.read_csv(filepath)
        
        # If multiple rows, return as list of dicts
        if len(df) > 1:
            return df.to_dict('records')
        # If single row, return as single dict
        elif len(df) == 1:
            return df.iloc[0].to_dict()
        else:
            return {}
    
    @staticmethod
    def parse_excel(filepath):
        """
        Parse Excel file to dictionary
        
        Args:
            filepath: Path to Excel file
            
        Returns:
            dict: Parsed data
        """
        df = pd.read_excel(filepath, engine='openpyxl')
        
        # If multiple rows, return as list of dicts
        if len(df) > 1:
            return df.to_dict('records')
        # If single row, return as single dict
        elif len(df) == 1:
            return df.iloc[0].to_dict()
        else:
            return {}
    
    @staticmethod
    def parse_txt(filepath):
        """
        Parse text file to dictionary
        Supports two formats:
        1. key:value format (e.g., "name: John")
        2. Line-by-line content (each line becomes "line_N: content")
        
        Args:
            filepath: Path to text file
            
        Returns:
            dict: Parsed data
        """
        data = {}
        line_number = 1
        has_key_value_pairs = False
        
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # First pass: check if file has key:value format
        for line in lines:
            line = line.strip()
            if line and ':' in line:
                has_key_value_pairs = True
                break
        
        # Parse based on detected format
        if has_key_value_pairs:
            # Parse as key:value format
            for line in lines:
                line = line.strip()
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
        else:
            # Parse as line-by-line content
            for line in lines:
                line = line.strip()
                if line:  # Skip empty lines
                    data[f'line_{line_number}'] = line
                    line_number += 1
        
        return data
    
    @classmethod
    def parse_file(cls, filepath):
        """
        Parse file based on its type
        
        Args:
            filepath: Path to file
            
        Returns:
            dict: Parsed data
            
        Raises:
            ValueError: If file type is not supported
        """
        file_type = cls.detect_file_type(filepath)
        
        if file_type == 'json':
            return cls.parse_json(filepath)
        elif file_type == 'csv':
            return cls.parse_csv(filepath)
        elif file_type == 'excel':
            return cls.parse_excel(filepath)
        elif file_type == 'txt':
            return cls.parse_txt(filepath)
        elif file_type == 'pdf':
            raise NotImplementedError("PDF parsing not yet implemented")
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
    
    @staticmethod
    def normalize_data(data):
        """
        Normalize data to consistent format
        Converts all numeric strings to actual numbers for comparison
        
        Args:
            data: Data to normalize (dict or list)
            
        Returns:
            Normalized data
        """
        if isinstance(data, dict):
            normalized = {}
            for key, value in data.items():
                # Try to convert string numbers to float/int
                if isinstance(value, str):
                    try:
                        # Try integer first
                        if '.' not in value:
                            normalized[key] = int(value)
                        else:
                            normalized[key] = float(value)
                    except ValueError:
                        normalized[key] = value
                elif isinstance(value, dict):
                    normalized[key] = FileParser.normalize_data(value)
                elif isinstance(value, list):
                    normalized[key] = [FileParser.normalize_data(item) for item in value]
                else:
                    normalized[key] = value
            return normalized
        elif isinstance(data, list):
            return [FileParser.normalize_data(item) for item in data]
        else:
            return data

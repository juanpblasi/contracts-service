"""
Contract comparison engine
"""
from typing import Dict, List, Any, Tuple


class ContractComparator:
    """Engine for comparing two contract documents"""
    
    def __init__(self):
        self.matches = []
        self.differences = []
        self.only_in_file1 = []
        self.only_in_file2 = []
    
    def compare(self, data1: Any, data2: Any, path: str = "") -> Dict:
        """
        Compare two data structures recursively
        
        Args:
            data1: First data structure
            data2: Second data structure
            path: Current path in nested structure (for tracking)
            
        Returns:
            dict: Comparison results
        """
        # Reset results
        self.matches = []
        self.differences = []
        self.only_in_file1 = []
        self.only_in_file2 = []
        
        # Perform comparison
        self._compare_recursive(data1, data2, path)
        
        # Calculate statistics
        total_fields = len(self.matches) + len(self.differences) + \
                      len(self.only_in_file1) + len(self.only_in_file2)
        
        match_percentage = (len(self.matches) / total_fields * 100) if total_fields > 0 else 0
        
        return {
            'matches': self.matches,
            'differences': self.differences,
            'only_in_file1': self.only_in_file1,
            'only_in_file2': self.only_in_file2,
            'statistics': {
                'total_fields': total_fields,
                'matches_count': len(self.matches),
                'differences_count': len(self.differences),
                'only_in_file1_count': len(self.only_in_file1),
                'only_in_file2_count': len(self.only_in_file2),
                'match_percentage': round(match_percentage, 2)
            }
        }
    
    def _compare_recursive(self, data1: Any, data2: Any, path: str = ""):
        """
        Recursively compare two data structures
        
        Args:
            data1: First data structure
            data2: Second data structure
            path: Current path in structure
        """
        # Handle lists
        if isinstance(data1, list) and isinstance(data2, list):
            self._compare_lists(data1, data2, path)
            return
        
        # Handle dictionaries
        if isinstance(data1, dict) and isinstance(data2, dict):
            self._compare_dicts(data1, data2, path)
            return
        
        # Direct comparison for primitive types
        if data1 == data2:
            self.matches.append({
                'field': path or 'root',
                'value': data1
            })
        else:
            self.differences.append({
                'field': path or 'root',
                'file1_value': data1,
                'file2_value': data2
            })
    
    def _compare_dicts(self, dict1: Dict, dict2: Dict, path: str):
        """
        Compare two dictionaries
        
        Args:
            dict1: First dictionary
            dict2: Second dictionary
            path: Current path in structure
        """
        # Get all keys
        keys1 = set(dict1.keys())
        keys2 = set(dict2.keys())
        
        # Keys in both
        common_keys = keys1 & keys2
        
        # Keys only in file1
        only_in_1 = keys1 - keys2
        
        # Keys only in file2
        only_in_2 = keys2 - keys1
        
        # Compare common keys
        for key in common_keys:
            new_path = f"{path}.{key}" if path else key
            value1 = dict1[key]
            value2 = dict2[key]
            
            # Recursive comparison
            if isinstance(value1, (dict, list)) or isinstance(value2, (dict, list)):
                self._compare_recursive(value1, value2, new_path)
            else:
                # Direct comparison
                if value1 == value2:
                    self.matches.append({
                        'field': new_path,
                        'value': value1
                    })
                else:
                    self.differences.append({
                        'field': new_path,
                        'file1_value': value1,
                        'file2_value': value2
                    })
        
        # Record fields only in file1
        for key in only_in_1:
            new_path = f"{path}.{key}" if path else key
            self.only_in_file1.append({
                'field': new_path,
                'value': dict1[key]
            })
        
        # Record fields only in file2
        for key in only_in_2:
            new_path = f"{path}.{key}" if path else key
            self.only_in_file2.append({
                'field': new_path,
                'value': dict2[key]
            })
    
    def _compare_lists(self, list1: List, list2: List, path: str):
        """
        Compare two lists
        
        Args:
            list1: First list
            list2: Second list
            path: Current path in structure
        """
        # Compare by index
        max_len = max(len(list1), len(list2))
        
        for i in range(max_len):
            new_path = f"{path}[{i}]"
            
            if i < len(list1) and i < len(list2):
                # Both have this index
                self._compare_recursive(list1[i], list2[i], new_path)
            elif i < len(list1):
                # Only in list1
                self.only_in_file1.append({
                    'field': new_path,
                    'value': list1[i]
                })
            else:
                # Only in list2
                self.only_in_file2.append({
                    'field': new_path,
                    'value': list2[i]
                })
    
    @staticmethod
    def generate_summary(comparison_result: Dict) -> str:
        """
        Generate a human-readable summary of comparison
        
        Args:
            comparison_result: Result from compare() method
            
        Returns:
            str: Summary text
        """
        stats = comparison_result['statistics']
        
        summary = f"""
Comparison Summary:
------------------
Total Fields Analyzed: {stats['total_fields']}
Matching Fields: {stats['matches_count']}
Different Fields: {stats['differences_count']}
Fields only in File 1: {stats['only_in_file1_count']}
Fields only in File 2: {stats['only_in_file2_count']}
Match Percentage: {stats['match_percentage']}%
"""
        return summary.strip()

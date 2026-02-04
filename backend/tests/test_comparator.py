"""
Tests for comparator module
"""
import pytest
from services.comparator import ContractComparator


class TestContractComparator:
    """Test cases for ContractComparator"""
    
    def test_compare_identical_dicts(self):
        """Test comparison of identical dictionaries"""
        comparator = ContractComparator()
        
        data1 = {'name': 'John', 'age': 30}
        data2 = {'name': 'John', 'age': 30}
        
        result = comparator.compare(data1, data2)
        
        assert result['statistics']['matches_count'] == 2
        assert result['statistics']['differences_count'] == 0
        assert result['statistics']['match_percentage'] == 100.0
    
    def test_compare_different_values(self):
        """Test comparison with different values"""
        comparator = ContractComparator()
        
        data1 = {'name': 'John', 'age': 30}
        data2 = {'name': 'Jane', 'age': 30}
        
        result = comparator.compare(data1, data2)
        
        assert result['statistics']['matches_count'] == 1
        assert result['statistics']['differences_count'] == 1
        assert len(result['differences']) == 1
        assert result['differences'][0]['field'] == 'name'
    
    def test_compare_missing_fields(self):
        """Test comparison with missing fields"""
        comparator = ContractComparator()
        
        data1 = {'name': 'John', 'age': 30, 'city': 'NYC'}
        data2 = {'name': 'John', 'age': 30}
        
        result = comparator.compare(data1, data2)
        
        assert result['statistics']['only_in_file1_count'] == 1
        assert result['only_in_file1'][0]['field'] == 'city'
    
    def test_compare_nested_structures(self):
        """Test comparison of nested structures"""
        comparator = ContractComparator()
        
        data1 = {
            'person': {
                'name': 'John',
                'address': {
                    'city': 'NYC'
                }
            }
        }
        
        data2 = {
            'person': {
                'name': 'John',
                'address': {
                    'city': 'LA'
                }
            }
        }
        
        result = comparator.compare(data1, data2)
        
        assert result['statistics']['differences_count'] == 1
        assert result['differences'][0]['field'] == 'person.address.city'
    
    def test_compare_lists(self):
        """Test comparison of lists"""
        comparator = ContractComparator()
        
        data1 = {'items': ['A', 'B', 'C']}
        data2 = {'items': ['A', 'B', 'D']}
        
        result = comparator.compare(data1, data2)
        
        # Should detect difference in third element
        assert result['statistics']['differences_count'] == 1
    
    def test_generate_summary(self):
        """Test summary generation"""
        comparator = ContractComparator()
        
        data1 = {'a': 1, 'b': 2}
        data2 = {'a': 1, 'b': 3}
        
        result = comparator.compare(data1, data2)
        summary = ContractComparator.generate_summary(result)
        
        assert 'Total Fields Analyzed' in summary
        assert 'Match Percentage' in summary

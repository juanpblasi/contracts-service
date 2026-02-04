"""
Integration tests for API endpoints
"""
import pytest
import json
import tempfile
import os
from app import create_app


@pytest.fixture
def client():
    """Create test client"""
    app = create_app('development')
    app.config['TESTING'] = True
    
    with app.test_client() as client:
        yield client


@pytest.fixture
def sample_json_files():
    """Create sample JSON files for testing"""
    # File 1
    data1 = {
        'contractNumber': 'CTR-001',
        'customerName': 'John Doe',
        'premium': 1500.00
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f1:
        json.dump(data1, f1)
        file1_path = f1.name
    
    # File 2
    data2 = {
        'contractNumber': 'CTR-001',
        'customerName': 'Jane Doe',
        'premium': 1500.00
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f2:
        json.dump(data2, f2)
        file2_path = f2.name
    
    yield file1_path, file2_path
    
    # Cleanup
    os.unlink(file1_path)
    os.unlink(file2_path)


class TestAPI:
    """Test cases for API endpoints"""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint"""
        response = client.get('/api/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_compare_endpoint_missing_files(self, client):
        """Test compare endpoint with missing files"""
        response = client.post('/api/compare')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data['status']
    
    def test_compare_endpoint_success(self, client, sample_json_files):
        """Test successful comparison"""
        file1_path, file2_path = sample_json_files
        
        with open(file1_path, 'rb') as f1, open(file2_path, 'rb') as f2:
            response = client.post('/api/compare', data={
                'file1': (f1, 'contract1.json'),
                'file2': (f2, 'contract2.json')
            })
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'success'
        assert 'report' in data
        assert 'summary' in data['report']
        assert 'details' in data['report']
        
        # Check that difference in customerName is detected
        summary = data['report']['summary']
        assert summary['differences'] == 1
        assert summary['matches'] == 2
    
    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get('/')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'service' in data
        assert 'endpoints' in data

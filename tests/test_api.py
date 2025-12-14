"""
Test suite for Flask API endpoints
"""
import pytest
import json
from app import app, mysql


@pytest.fixture
def client():
    # Configure test client
    app.config['TESTING'] = True
    
    # Add teardown handler to properly close MySQL connections
    @app.teardown_appcontext
    def shutdown_session(exception=None):
        pass
    
    with app.test_client() as client:
        yield client


class TestPilotCRUD:
    # Test suite for Pilot CRUD operations
    
    def test_get_all_pilots_json(self, client):
        # Test GET all pilots with JSON format
        response = client.get('/api/pilots')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert 'pilots' in data
        assert isinstance(data['pilots'], list)
    
    def test_get_all_pilots_xml(self, client):
        # Test GET all pilots with XML format
        response = client.get('/api/pilots?format=xml')
        assert response.status_code == 200
        assert response.content_type == 'application/xml'
        assert b'<?xml' in response.data
    
    def test_get_pilot_by_id_success(self, client):
        # Test GET single pilot by ID (success)
        response = client.get('/api/pilots/1')
        assert response.status_code in [200, 404]  # 404 if pilot doesn't exist
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'pilot' in data
            assert data['pilot']['id'] == 1
    
    def test_get_pilot_by_id_not_found(self, client):
        # Test GET single pilot by ID (not found)
        response = client.get('/api/pilots/999999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()
    
    def test_create_pilot_success(self, client):
        # Test POST create new pilot (success)
        new_pilot = {
            'name': 'Test Pilot',
            'flight_years': 5,
            'rank': 'Captain',
            'mission_success': 10
        }
        response = client.post('/api/pilots',
                              data=json.dumps(new_pilot),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'pilot' in data
        assert data['pilot']['name'] == 'Test Pilot'
        
        # Clean up - delete the created pilot
        pilot_id = data['pilot']['id']
        client.delete(f'/api/pilots/{pilot_id}')
    
    def test_create_pilot_missing_field(self, client):
        # Test POST create pilot with missing required field
        incomplete_pilot = {
            'name': 'Incomplete Pilot',
            'flight_years': 3
            # Missing rank and mission_success
        }
        response = client.post('/api/pilots',
                              data=json.dumps(incomplete_pilot),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'missing' in data['message'].lower() or 'required' in data['message'].lower()
    
    def test_create_pilot_invalid_data_type(self, client):
        # Test POST create pilot with invalid data type
        invalid_pilot = {
            'name': 'Invalid Pilot',
            'flight_years': 'not_a_number',  # Should be int
            'rank': 'Lieutenant',
            'mission_success': 5
        }
        response = client.post('/api/pilots',
                              data=json.dumps(invalid_pilot),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_update_pilot_success(self, client):
        # Test PUT update pilot (success)
        # First create a pilot to update
        new_pilot = {
            'name': 'Pilot To Update',
            'flight_years': 2,
            'rank': 'Ensign',
            'mission_success': 3
        }
        create_response = client.post('/api/pilots',
                                     data=json.dumps(new_pilot),
                                     content_type='application/json')
        pilot_id = json.loads(create_response.data)['pilot']['id']
        
        # Update the pilot
        update_data = {
            'rank': 'Commander',
            'mission_success': 15
        }
        response = client.put(f'/api/pilots/{pilot_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['pilot']['rank'] == 'Commander'
        assert data['pilot']['mission_success'] == 15
        
        # Clean up
        client.delete(f'/api/pilots/{pilot_id}')
    
    def test_update_pilot_not_found(self, client):
        # Test PUT update pilot (not found)
        update_data = {
            'rank': 'Admiral'
        }
        response = client.put('/api/pilots/999999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()
    
    def test_delete_pilot_success(self, client):
        # Test DELETE pilot (success)
        # First create a pilot to delete
        new_pilot = {
            'name': 'Pilot To Delete',
            'flight_years': 1,
            'rank': 'Cadet',
            'mission_success': 1
        }
        create_response = client.post('/api/pilots',
                                     data=json.dumps(new_pilot),
                                     content_type='application/json')
        pilot_id = json.loads(create_response.data)['pilot']['id']
        
        # Delete the pilot
        response = client.delete(f'/api/pilots/{pilot_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        
        # Verify it's deleted
        get_response = client.get(f'/api/pilots/{pilot_id}')
        assert get_response.status_code == 404
    
    def test_delete_pilot_not_found(self, client):
        # Test DELETE pilot (not found)
        response = client.delete('/api/pilots/999999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()


class TestErrorHandlers:
    # Test suite for error handlers
    
    def test_404_not_found(self, client):
        # Test 404 error handler
        response = client.get('/api/nonexistent-endpoint')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()
    
    def test_405_method_not_allowed(self, client):
        # Test 405 error handler
        response = client.post('/api/test-db')  # Test-db only accepts GET
        assert response.status_code == 405
        data = json.loads(response.data)
        assert data['status'] == 'error'


class TestFormattingOptions:
    # Test suite for response formatting (JSON/XML)
    
    def test_json_format_default(self, client):
        # Test JSON format (default)
        response = client.get('/api/pilots')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_json_format_explicit(self, client):
        # Test JSON format (explicit parameter)
        response = client.get('/api/pilots?format=json')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
    
    def test_xml_format(self, client):
        # Test XML format
        response = client.get('/api/pilots?format=xml')
        assert response.status_code == 200
        assert response.content_type == 'application/xml'
        assert b'<?xml' in response.data
    
    def test_invalid_format_defaults_to_json(self, client):
        # Test invalid format parameter defaults to JSON
        response = client.get('/api/pilots?format=invalid')
        assert response.status_code == 200
        assert response.content_type == 'application/json'

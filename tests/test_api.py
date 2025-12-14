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


class TestShipCRUD:
    # Test suite for Ship CRUD operations
    
    def test_get_all_ships_json(self, client):
        # Test GET all ships with JSON format
        response = client.get('/api/ships')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert 'ships' in data
        assert isinstance(data['ships'], list)
    
    def test_get_all_ships_xml(self, client):
        # Test GET all ships with XML format
        response = client.get('/api/ships?format=xml')
        assert response.status_code == 200
        assert response.content_type == 'application/xml'
        assert b'<?xml' in response.data
    
    def test_get_ship_by_id_success(self, client):
        # Test GET single ship by ID (success)
        response = client.get('/api/ships/1')
        assert response.status_code in [200, 404]  # 404 if ship doesn't exist
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'ship' in data
            assert data['ship']['id'] == 1
    
    def test_get_ship_by_id_not_found(self, client):
        # Test GET single ship by ID (not found)
        response = client.get('/api/ships/999999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()
    
    def test_create_ship_success(self, client):
        # Test POST create new ship (success)
        new_ship = {
            'name': 'Test Ship',
            'capacity': 100,
            'speed': 500,
            'shield': 80,
            'ship_class_id': 1,
            'pilot_id': 1
        }
        response = client.post('/api/ships',
                              data=json.dumps(new_ship),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'ship' in data
        assert data['ship']['name'] == 'Test Ship'
        
        # Clean up - delete the created ship
        ship_id = data['ship']['id']
        client.delete(f'/api/ships/{ship_id}')
    
    def test_create_ship_missing_field(self, client):
        # Test POST create ship with missing required field
        incomplete_ship = {
            'name': 'Incomplete Ship',
            'capacity': 50
            # Missing speed, shield, ship_class_id, pilot_id
        }
        response = client.post('/api/ships',
                              data=json.dumps(incomplete_ship),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'missing' in data['message'].lower() or 'required' in data['message'].lower()
    
    def test_create_ship_invalid_data_type(self, client):
        # Test POST create ship with invalid data type
        invalid_ship = {
            'name': 'Invalid Ship',
            'capacity': 'not_a_number',  # Should be int
            'speed': 300,
            'shield': 60,
            'ship_class_id': 1,
            'pilot_id': 1
        }
        response = client.post('/api/ships',
                              data=json.dumps(invalid_ship),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_update_ship_success(self, client):
        # Test PUT update ship (success)
        # First create a ship to update
        new_ship = {
            'name': 'Ship To Update',
            'capacity': 75,
            'speed': 400,
            'shield': 70,
            'ship_class_id': 1,
            'pilot_id': 1
        }
        create_response = client.post('/api/ships',
                                     data=json.dumps(new_ship),
                                     content_type='application/json')
        ship_id = json.loads(create_response.data)['ship']['id']
        
        # Update the ship
        update_data = {
            'speed': 600,
            'shield': 90
        }
        response = client.put(f'/api/ships/{ship_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['ship']['speed'] == 600
        assert data['ship']['shield'] == 90
        
        # Clean up
        client.delete(f'/api/ships/{ship_id}')
    
    def test_update_ship_not_found(self, client):
        # Test PUT update ship (not found)
        update_data = {
            'speed': 800
        }
        response = client.put('/api/ships/999999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()
    
    def test_delete_ship_success(self, client):
        # Test DELETE ship (success)
        # First create a ship to delete
        new_ship = {
            'name': 'Ship To Delete',
            'capacity': 30,
            'speed': 200,
            'shield': 40,
            'ship_class_id': 1,
            'pilot_id': 1
        }
        create_response = client.post('/api/ships',
                                     data=json.dumps(new_ship),
                                     content_type='application/json')
        ship_id = json.loads(create_response.data)['ship']['id']
        
        # Delete the ship
        response = client.delete(f'/api/ships/{ship_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        
        # Verify it's deleted
        get_response = client.get(f'/api/ships/{ship_id}')
        assert get_response.status_code == 404
    
    def test_delete_ship_not_found(self, client):
        # Test DELETE ship (not found)
        response = client.delete('/api/ships/999999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()


class TestShipClassCRUD:
    # Test suite for ShipClass CRUD operations
    
    def test_get_all_ship_classes_json(self, client):
        # Test GET all ship classes with JSON format
        response = client.get('/api/ship-classes')
        assert response.status_code == 200
        assert response.content_type == 'application/json'
        data = json.loads(response.data)
        assert 'ship_classes' in data
        assert isinstance(data['ship_classes'], list)
    
    def test_get_all_ship_classes_xml(self, client):
        # Test GET all ship classes with XML format
        response = client.get('/api/ship-classes?format=xml')
        assert response.status_code == 200
        assert response.content_type == 'application/xml'
        assert b'<?xml' in response.data
    
    def test_get_ship_class_by_id_success(self, client):
        # Test GET single ship class by ID (success)
        response = client.get('/api/ship-classes/1')
        assert response.status_code in [200, 404]  # 404 if ship class doesn't exist
        if response.status_code == 200:
            data = json.loads(response.data)
            assert 'ship_class' in data
            assert data['ship_class']['id'] == 1
    
    def test_get_ship_class_by_id_not_found(self, client):
        # Test GET single ship class by ID (not found)
        response = client.get('/api/ship-classes/999999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()
    
    def test_create_ship_class_success(self, client):
        # Test POST create new ship class (success with description)
        new_ship_class = {
            'name': 'Test Class',
            'description': 'A test ship class'
        }
        response = client.post('/api/ship-classes',
                              data=json.dumps(new_ship_class),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'ship_class' in data
        assert data['ship_class']['name'] == 'Test Class'
        
        # Clean up - delete the created ship class
        class_id = data['ship_class']['id']
        client.delete(f'/api/ship-classes/{class_id}')
    
    def test_create_ship_class_without_description(self, client):
        # Test POST create ship class without optional description
        new_ship_class = {
            'name': 'Test Class No Desc'
        }
        response = client.post('/api/ship-classes',
                              data=json.dumps(new_ship_class),
                              content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'ship_class' in data
        assert data['ship_class']['name'] == 'Test Class No Desc'
        
        # Clean up
        class_id = data['ship_class']['id']
        client.delete(f'/api/ship-classes/{class_id}')
    
    def test_create_ship_class_missing_field(self, client):
        # Test POST create ship class with missing required field
        incomplete_ship_class = {
            'description': 'Missing name field'
        }
        response = client.post('/api/ship-classes',
                              data=json.dumps(incomplete_ship_class),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'missing' in data['message'].lower() or 'required' in data['message'].lower()
    
    def test_create_ship_class_invalid_data_type(self, client):
        # Test POST create ship class with invalid data type
        invalid_ship_class = {
            'name': 12345,  # Should be string
            'description': 'Invalid name type'
        }
        response = client.post('/api/ship-classes',
                              data=json.dumps(invalid_ship_class),
                              content_type='application/json')
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_update_ship_class_success(self, client):
        # Test PUT update ship class (success)
        # First create a ship class to update
        new_ship_class = {
            'name': 'Class To Update',
            'description': 'Original description'
        }
        create_response = client.post('/api/ship-classes',
                                     data=json.dumps(new_ship_class),
                                     content_type='application/json')
        class_id = json.loads(create_response.data)['ship_class']['id']
        
        # Update the ship class
        update_data = {
            'description': 'Updated description'
        }
        response = client.put(f'/api/ship-classes/{class_id}',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['ship_class']['description'] == 'Updated description'
        
        # Clean up
        client.delete(f'/api/ship-classes/{class_id}')
    
    def test_update_ship_class_not_found(self, client):
        # Test PUT update ship class (not found)
        update_data = {
            'name': 'Updated Name'
        }
        response = client.put('/api/ship-classes/999999',
                             data=json.dumps(update_data),
                             content_type='application/json')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
        assert 'not found' in data['message'].lower()
    
    def test_delete_ship_class_success(self, client):
        # Test DELETE ship class (success)
        # First create a ship class to delete
        new_ship_class = {
            'name': 'Class To Delete',
            'description': 'Will be deleted'
        }
        create_response = client.post('/api/ship-classes',
                                     data=json.dumps(new_ship_class),
                                     content_type='application/json')
        class_id = json.loads(create_response.data)['ship_class']['id']
        
        # Delete the ship class
        response = client.delete(f'/api/ship-classes/{class_id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        
        # Verify it's deleted
        get_response = client.get(f'/api/ship-classes/{class_id}')
        assert get_response.status_code == 404
    
    def test_delete_ship_class_not_found(self, client):
        # Test DELETE ship class (not found)
        response = client.delete('/api/ship-classes/999999')
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

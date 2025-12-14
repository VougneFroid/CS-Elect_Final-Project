"""
Comprehensive Test Suite for Ship Management API
Tests all endpoints including authentication, CRUD operations, and data validation
"""
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import json
from app import app, mysql


@pytest.fixture(scope='function')
def client():
    """Configure test client"""
    app.config['TESTING'] = True
    app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = False
    with app.test_client() as client:
        yield client


@pytest.fixture
def auth_token(client):
    """Get authentication token for protected endpoints"""
    # First, register a test user
    register_data = {
        'username': 'testuser_pytest',
        'email': 'testuser_pytest@example.com',
        'password': 'TestPassword123!'
    }
    
    # Try to register (might already exist from previous tests)
    client.post('/api/auth/register', 
                json=register_data,
                content_type='application/json')
    
    # Login to get token
    login_data = {
        'username': 'testuser_pytest',
        'password': 'TestPassword123!'
    }
    
    response = client.post('/api/auth/login',
                          json=login_data,
                          content_type='application/json')
    
    data = json.loads(response.data)
    return data.get('token', '')


class TestBasicEndpoints:
    """Test basic non-authenticated endpoints"""
    
    def test_home_endpoint(self, client):
        """Test home endpoint"""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Hello, Flask!' in response.data
    
    def test_database_connection(self, client):
        """Test database connection endpoint"""
        response = client.get('/api/test-db')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['message'] == 'Database connection successful'


class TestAuthentication:
    """Test authentication endpoints"""
    
    def test_register_success(self, client):
        """Test successful user registration"""
        data = {
            'username': f'newuser_{os.urandom(4).hex()}',
            'email': f'newuser_{os.urandom(4).hex()}@example.com',
            'password': 'SecurePass123!'
        }
        
        response = client.post('/api/auth/register',
                              json=data,
                              content_type='application/json')
        
        assert response.status_code == 201
        response_data = json.loads(response.data)
        assert response_data['status'] == 'success'
        assert 'user' in response_data
    
    def test_register_missing_fields(self, client):
        """Test registration with missing required fields"""
        data = {'username': 'testuser'}  # Missing email and password
        
        response = client.post('/api/auth/register',
                              json=data,
                              content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['status'] == 'error'
    
    def test_register_invalid_username(self, client):
        """Test registration with invalid username (too short)"""
        data = {
            'username': 'ab',  # Too short
            'email': 'test@example.com',
            'password': 'password123'
        }
        
        response = client.post('/api/auth/register',
                              json=data,
                              content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['status'] == 'error'
    
    def test_login_success(self, client, auth_token):
        """Test successful login"""
        # auth_token fixture already performs login
        assert auth_token is not None
        assert len(auth_token) > 0
    
    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        data = {
            'username': 'nonexistent_user',
            'password': 'wrongpassword'
        }
        
        response = client.post('/api/auth/login',
                              json=data,
                              content_type='application/json')
        
        assert response.status_code == 401
        response_data = json.loads(response.data)
        assert response_data['status'] == 'error'
    
    def test_login_missing_fields(self, client):
        """Test login with missing fields"""
        data = {'username': 'testuser'}  # Missing password
        
        response = client.post('/api/auth/login',
                              json=data,
                              content_type='application/json')
        
        assert response.status_code == 400
        response_data = json.loads(response.data)
        assert response_data['status'] == 'error'


class TestPilotEndpoints:
    """Test pilot CRUD operations"""
    
    def test_get_all_pilots(self, client):
        """Test getting all pilots"""
        response = client.get('/api/pilots')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'pilots' in data
        assert isinstance(data['pilots'], list)
    
    def test_get_all_pilots_with_format(self, client):
        """Test getting pilots with XML format"""
        response = client.get('/api/pilots?format=xml')
        assert response.status_code == 200
        assert b'<?xml' in response.data
    
    def test_get_pilots_with_search(self, client):
        """Test searching pilots by name"""
        response = client.get('/api/pilots?name=Vougne')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'pilots' in data
    
    def test_get_pilot_by_id(self, client):
        """Test getting a specific pilot"""
        response = client.get('/api/pilots/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'pilot' in data
        assert data['pilot']['id'] == 1
    
    def test_get_pilot_not_found(self, client):
        """Test getting a non-existent pilot"""
        response = client.get('/api/pilots/999999')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_create_pilot_success(self, client, auth_token):
        """Test creating a new pilot"""
        pilot_data = {
            'name': f'Test Pilot {os.urandom(4).hex()}',
            'flight_years': 15,
            'rank': 'Captain',
            'mission_success': 50
        }
        
        response = client.post('/api/pilots',
                              json=pilot_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'pilot' in data
    
    def test_create_pilot_unauthorized(self, client):
        """Test creating pilot without authentication"""
        pilot_data = {
            'name': 'Unauthorized Pilot',
            'flight_years': 10,
            'rank': 'Lieutenant',
            'mission_success': 20
        }
        
        response = client.post('/api/pilots',
                              json=pilot_data,
                              content_type='application/json')
        
        assert response.status_code == 401
    
    def test_create_pilot_missing_fields(self, client, auth_token):
        """Test creating pilot with missing required fields"""
        pilot_data = {
            'name': 'Incomplete Pilot'
            # Missing flight_years, rank, mission_success
        }
        
        response = client.post('/api/pilots',
                              json=pilot_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['status'] == 'error'
    
    def test_create_pilot_invalid_data_type(self, client, auth_token):
        """Test creating pilot with invalid data types"""
        pilot_data = {
            'name': 'Test Pilot',
            'flight_years': 'not_a_number',  # Should be int
            'rank': 'Captain',
            'mission_success': 50
        }
        
        response = client.post('/api/pilots',
                              json=pilot_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_update_pilot_success(self, client, auth_token):
        """Test updating an existing pilot"""
        # First create a pilot
        pilot_data = {
            'name': f'Pilot To Update {os.urandom(4).hex()}',
            'flight_years': 5,
            'rank': 'Ensign',
            'mission_success': 10
        }
        
        create_response = client.post('/api/pilots',
                                     json=pilot_data,
                                     headers={'Authorization': f'Bearer {auth_token}'},
                                     content_type='application/json')
        
        created_pilot = json.loads(create_response.data)['data']['pilot']
        pilot_id = created_pilot['id']
        
        # Update the pilot
        update_data = {
            'rank': 'Lieutenant',
            'mission_success': 25
        }
        
        response = client.put(f'/api/pilots/{pilot_id}',
                             json=update_data,
                             headers={'Authorization': f'Bearer {auth_token}'},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert data['pilot']['rank'] == 'Lieutenant'
        assert data['pilot']['mission_success'] == 25
    
    def test_update_pilot_not_found(self, client, auth_token):
        """Test updating a non-existent pilot"""
        update_data = {'rank': 'Admiral'}
        
        response = client.put('/api/pilots/999999',
                             json=update_data,
                             headers={'Authorization': f'Bearer {auth_token}'},
                             content_type='application/json')
        
        assert response.status_code == 404
    
    def test_delete_pilot_success(self, client, auth_token):
        """Test deleting a pilot"""
        # First create a pilot
        pilot_data = {
            'name': f'Pilot To Delete {os.urandom(4).hex()}',
            'flight_years': 1,
            'rank': 'Cadet',
            'mission_success': 1
        }
        
        create_response = client.post('/api/pilots',
                                     json=pilot_data,
                                     headers={'Authorization': f'Bearer {auth_token}'},
                                     content_type='application/json')
        
        created_pilot = json.loads(create_response.data)['data']['pilot']
        pilot_id = created_pilot['id']
        
        # Delete the pilot
        response = client.delete(f'/api/pilots/{pilot_id}',
                                headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'success'


class TestShipEndpoints:
    """Test ship CRUD operations"""
    
    def test_get_all_ships(self, client):
        """Test getting all ships"""
        response = client.get('/api/ships')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ships' in data
        assert isinstance(data['ships'], list)
    
    def test_get_ships_with_pagination(self, client):
        """Test getting ships with pagination parameters"""
        response = client.get('/api/ships?page=1&per_page=5')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ships' in data
        # Note: API doesn't currently return pagination metadata
        assert isinstance(data['ships'], list)
    
    def test_get_ship_by_id(self, client):
        """Test getting a specific ship"""
        response = client.get('/api/ships/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ship' in data
        assert data['ship']['id'] == 1
    
    def test_create_ship_success(self, client, auth_token):
        """Test creating a new ship"""
        ship_data = {
            'name': f'Test Ship {os.urandom(4).hex()}',
            'capacity': 150,
            'speed': 500,
            'shield': 100,
            'ship_class_id': 1,
            'pilot_id': 1
        }
        
        response = client.post('/api/ships',
                              json=ship_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
        assert 'ship' in data
    
    def test_create_ship_missing_fields(self, client, auth_token):
        """Test creating ship with missing fields"""
        ship_data = {
            'name': 'Incomplete Ship',
            'capacity': 100
            # Missing speed, shield, ship_class_id, pilot_id
        }
        
        response = client.post('/api/ships',
                              json=ship_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_create_ship_negative_values(self, client, auth_token):
        """Test creating ship with negative values"""
        ship_data = {
            'name': 'Invalid Ship',
            'capacity': -100,  # Invalid
            'speed': 500,
            'shield': 100,
            'ship_class_id': 1,
            'pilot_id': 1
        }
        
        response = client.post('/api/ships',
                              json=ship_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_update_ship_success(self, client, auth_token):
        """Test updating a ship"""
        # Create a ship first
        ship_data = {
            'name': f'Ship To Update {os.urandom(4).hex()}',
            'capacity': 100,
            'speed': 400,
            'shield': 80,
            'ship_class_id': 1,
            'pilot_id': 1
        }
        
        create_response = client.post('/api/ships',
                                     json=ship_data,
                                     headers={'Authorization': f'Bearer {auth_token}'},
                                     content_type='application/json')
        
        created_ship = json.loads(create_response.data)['data']['ship']
        ship_id = created_ship['id']
        
        # Update the ship
        update_data = {
            'speed': 600,
            'shield': 120
        }
        
        response = client.put(f'/api/ships/{ship_id}',
                             json=update_data,
                             headers={'Authorization': f'Bearer {auth_token}'},
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['ship']['speed'] == 600
        assert data['ship']['shield'] == 120
    
    def test_delete_ship_success(self, client, auth_token):
        """Test deleting a ship"""
        # Create a ship first
        ship_data = {
            'name': f'Ship To Delete {os.urandom(4).hex()}',
            'capacity': 50,
            'speed': 300,
            'shield': 60,
            'ship_class_id': 1,
            'pilot_id': 1
        }
        
        create_response = client.post('/api/ships',
                                     json=ship_data,
                                     headers={'Authorization': f'Bearer {auth_token}'},
                                     content_type='application/json')
        
        created_ship = json.loads(create_response.data)['data']['ship']
        ship_id = created_ship['id']
        
        # Delete the ship
        response = client.delete(f'/api/ships/{ship_id}',
                                headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200


class TestShipClassEndpoints:
    """Test ship class CRUD operations"""
    
    def test_get_all_ship_classes(self, client):
        """Test getting all ship classes"""
        response = client.get('/api/ship-classes')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ship_classes' in data
        assert isinstance(data['ship_classes'], list)
    
    def test_get_ship_class_by_id(self, client):
        """Test getting a specific ship class"""
        response = client.get('/api/ship-classes/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ship_class' in data
    
    def test_create_ship_class_success(self, client, auth_token):
        """Test creating a new ship class"""
        class_data = {
            'name': f'Test Class {os.urandom(4).hex()}',
            'description': 'A test ship class'
        }
        
        response = client.post('/api/ship-classes',
                              json=class_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_create_ship_class_without_description(self, client, auth_token):
        """Test creating ship class without optional description"""
        class_data = {
            'name': f'Test Class No Desc {os.urandom(4).hex()}'
        }
        
        response = client.post('/api/ship-classes',
                              json=class_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 201
    
    def test_update_ship_class_success(self, client, auth_token):
        """Test updating a ship class"""
        # Create first
        class_data = {
            'name': f'Class To Update {os.urandom(4).hex()}',
            'description': 'Original description'
        }
        
        create_response = client.post('/api/ship-classes',
                                     json=class_data,
                                     headers={'Authorization': f'Bearer {auth_token}'},
                                     content_type='application/json')
        
        created_class = json.loads(create_response.data)['data']['ship_class']
        class_id = created_class['id']
        
        # Update
        update_data = {'description': 'Updated description'}
        
        response = client.put(f'/api/ship-classes/{class_id}',
                             json=update_data,
                             headers={'Authorization': f'Bearer {auth_token}'},
                             content_type='application/json')
        
        assert response.status_code == 200
    
    def test_delete_ship_class_success(self, client, auth_token):
        """Test deleting a ship class"""
        # Create first
        class_data = {
            'name': f'Class To Delete {os.urandom(4).hex()}',
            'description': 'Will be deleted'
        }
        
        create_response = client.post('/api/ship-classes',
                                     json=class_data,
                                     headers={'Authorization': f'Bearer {auth_token}'},
                                     content_type='application/json')
        
        created_class = json.loads(create_response.data)['data']['ship_class']
        class_id = created_class['id']
        
        # Delete
        response = client.delete(f'/api/ship-classes/{class_id}',
                                headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200


class TestWeaponClassEndpoints:
    """Test weapon class CRUD operations"""
    
    def test_get_all_weapon_classes(self, client):
        """Test getting all weapon classes"""
        response = client.get('/api/weapon-classes')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'weapon_classes' in data
    
    def test_get_weapon_class_by_id(self, client):
        """Test getting a specific weapon class"""
        response = client.get('/api/weapon-classes/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'weapon_class' in data
    
    def test_create_weapon_class_success(self, client, auth_token):
        """Test creating a new weapon class"""
        weapon_data = {
            'class': f'Test Laser {os.urandom(4).hex()}',
            'damage': 100,
            'reload_speed': 5,
            'spread': 10,
            'range': 2000
        }
        
        response = client.post('/api/weapon-classes',
                              json=weapon_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_create_weapon_class_missing_fields(self, client, auth_token):
        """Test creating weapon class with missing fields"""
        weapon_data = {
            'class': 'Incomplete Weapon',
            'damage': 50
            # Missing reload_speed, spread, range
        }
        
        response = client.post('/api/weapon-classes',
                              json=weapon_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_update_weapon_class_success(self, client, auth_token):
        """Test updating a weapon class"""
        # Create first
        weapon_data = {
            'class': f'Weapon To Update {os.urandom(4).hex()}',
            'damage': 75,
            'reload_speed': 8,
            'spread': 5,
            'range': 1500
        }
        
        create_response = client.post('/api/weapon-classes',
                                     json=weapon_data,
                                     headers={'Authorization': f'Bearer {auth_token}'},
                                     content_type='application/json')
        
        created_weapon = json.loads(create_response.data)['data']['weapon_class']
        weapon_id = created_weapon['id']
        
        # Update
        update_data = {'damage': 150, 'range': 2500}
        
        response = client.put(f'/api/weapon-classes/{weapon_id}',
                             json=update_data,
                             headers={'Authorization': f'Bearer {auth_token}'},
                             content_type='application/json')
        
        assert response.status_code == 200
    
    def test_delete_weapon_class_success(self, client, auth_token):
        """Test deleting a weapon class"""
        # Create first
        weapon_data = {
            'class': f'Weapon To Delete {os.urandom(4).hex()}',
            'damage': 50,
            'reload_speed': 10,
            'spread': 3,
            'range': 1000
        }
        
        create_response = client.post('/api/weapon-classes',
                                     json=weapon_data,
                                     headers={'Authorization': f'Bearer {auth_token}'},
                                     content_type='application/json')
        
        created_weapon = json.loads(create_response.data)['data']['weapon_class']
        weapon_id = created_weapon['id']
        
        # Delete
        response = client.delete(f'/api/weapon-classes/{weapon_id}',
                                headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 200


class TestShipWeaponsEndpoints:
    """Test ship-weapons relationship operations"""
    
    def test_get_all_ship_weapons(self, client):
        """Test getting all ship-weapon assignments"""
        response = client.get('/api/ship-weapons')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ship_weapons' in data
    
    def test_get_ship_weapons_by_ship_id(self, client):
        """Test getting weapons for a specific ship"""
        response = client.get('/api/ship-weapons/ship/1')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'ship_weapons' in data
    
    def test_create_ship_weapon_success(self, client, auth_token):
        """Test creating a ship-weapon assignment"""
        # First create a ship
        ship_data = {
            'name': f'Armed Ship {os.urandom(4).hex()}',
            'capacity': 100,
            'speed': 500,
            'shield': 100,
            'ship_class_id': 1,
            'pilot_id': 1
        }
        
        ship_response = client.post('/api/ships',
                                   json=ship_data,
                                   headers={'Authorization': f'Bearer {auth_token}'},
                                   content_type='application/json')
        
        ship_id = json.loads(ship_response.data)['ship']['id']
        
        # Assign weapon
        weapon_assignment = {
            'ship_id': ship_id,
            'ship_class_id': 1,
            'weapon_class_id': 1,
            'name': f'Test Weapon {os.urandom(4).hex()}'
        }
        
        response = client.post('/api/ship-weapons',
                              json=weapon_assignment,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data['status'] == 'success'
    
    def test_create_ship_weapon_missing_fields(self, client, auth_token):
        """Test creating ship-weapon with missing fields"""
        weapon_assignment = {
            'ship_id': 1,
            'ship_class_id': 1
            # Missing weapon_class_id and name
        }
        
        response = client.post('/api/ship-weapons',
                              json=weapon_assignment,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_delete_ship_weapon_not_found(self, client, auth_token):
        """Test deleting non-existent ship-weapon assignment"""
        response = client.delete('/api/ship-weapons/999999/999999/999999',
                                headers={'Authorization': f'Bearer {auth_token}'})
        
        assert response.status_code == 404


class TestDataValidation:
    """Test data validation rules"""
    
    def test_pilot_negative_flight_years(self, client, auth_token):
        """Test that negative flight years are rejected"""
        pilot_data = {
            'name': 'Invalid Pilot',
            'flight_years': -5,
            'rank': 'Captain',
            'mission_success': 10
        }
        
        response = client.post('/api/pilots',
                              json=pilot_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_pilot_empty_name(self, client, auth_token):
        """Test that empty names are rejected"""
        pilot_data = {
            'name': '',
            'flight_years': 5,
            'rank': 'Captain',
            'mission_success': 10
        }
        
        response = client.post('/api/pilots',
                              json=pilot_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        assert response.status_code == 400
    
    def test_ship_invalid_foreign_keys(self, client, auth_token):
        """Test that invalid foreign keys are handled"""
        ship_data = {
            'name': 'Invalid Ship',
            'capacity': 100,
            'speed': 500,
            'shield': 100,
            'ship_class_id': 999999,  # Non-existent
            'pilot_id': 999999  # Non-existent
        }
        
        response = client.post('/api/ships',
                              json=ship_data,
                              headers={'Authorization': f'Bearer {auth_token}'},
                              content_type='application/json')
        
        # Should fail due to foreign key constraints
        assert response.status_code in [400, 500]


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_not_found(self, client):
        """Test 404 error for non-existent endpoint"""
        response = client.get('/api/nonexistent')
        assert response.status_code == 404
    
    def test_405_method_not_allowed(self, client):
        """Test 405 error for wrong HTTP method"""
        response = client.delete('/')
        assert response.status_code == 405
    
    def test_unauthorized_access(self, client):
        """Test accessing protected endpoint without token"""
        response = client.post('/api/pilots',
                              json={'name': 'Test'},
                              content_type='application/json')
        
        assert response.status_code == 401


if __name__ == '__main__':
    # Run tests with pytest
    pytest.main([__file__, '-v', '--tb=short'])

import json
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from utils.formatters import format_response, row_to_dict, rows_to_dict_list
from utils.validators import validate_pilot_data, validate_ship_data, validate_ship_class_data, validate_weapon_class_data
from models import pilot, ship, ship_class, weapon_class, ship_weapons

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vondev'
app.config['MYSQL_DB'] = 'shiperd'

mysql = MySQL(app)

# Teardown handler for MySQL connections
@app.teardown_appcontext
def close_db(error):
    # Close database connection after each request
    pass

# Column definitions
PILOT_COLUMNS = ['id', 'name', 'flight_years', 'rank', 'mission_success']
SHIP_COLUMNS = ['id', 'name', 'capacity', 'speed', 'shield', 'ship_class_id', 'ship_class_name', 'pilot_id', 'pilot_name']
SHIP_CLASS_COLUMNS = ['id', 'name', 'description']
WEAPON_CLASS_COLUMNS = ['id', 'class', 'damage', 'reload_speed', 'spread', 'range']
SHIP_WEAPONS_COLUMNS = ['ship_id', 'ship_name', 'ship_class_id', 'ship_class_name', 'weapon_class_id', 'weapon_class_name', 'name']

@app.route('/')
def home():
    return "Hello, Flask!"

@app.route('/api/test-db')
def test_db():
    """Test database connection endpoint"""
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        cursor.close()
        
        if result:
            return jsonify({
                'status': 'success',
                'message': 'Database connection successful',
                'result': result[0]
            }), 200
        else:
            return jsonify({
                'status': 'error',
                'message': 'Database query returned no result'
            }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Database connection failed: {str(e)}'
        }), 500

# Pilot Endpoints
@app.route('/api/pilots', methods=['GET'])
def get_pilots():
    # Get all pilots or search with criteria
    try:
        # Check for search parameters
        criteria = {}
        
        # Name search (string)
        if request.args.get('name'):
            criteria['name'] = request.args.get('name')
        
        # Rank search (string)
        if request.args.get('rank'):
            criteria['rank'] = request.args.get('rank')
        
        # Minimum flight years (numeric)
        if request.args.get('min_flight_years'):
            try:
                criteria['min_flight_years'] = int(request.args.get('min_flight_years'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'min_flight_years must be a valid integer'
                }, 400)
        
        # Minimum mission success (numeric)
        if request.args.get('min_mission_success'):
            try:
                criteria['min_mission_success'] = int(request.args.get('min_mission_success'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'min_mission_success must be a valid integer'
                }, 400)
        
        # Use search if criteria provided, otherwise get all
        if criteria:
            pilots_data = pilot.search(mysql, criteria)
        else:
            pilots_data = pilot.get_all(mysql)
        
        pilots_list = rows_to_dict_list(pilots_data, PILOT_COLUMNS)
        return format_response({'pilots': pilots_list}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve pilots: {str(e)}'
        }, 500)

@app.route('/api/pilots/<int:pilot_id>', methods=['GET'])
def get_pilot(pilot_id):
    # Get a single pilot by ID
    try:
        pilot_data = pilot.get_by_id(mysql, pilot_id)
        if pilot_data is None:
            return format_response({
                'status': 'error',
                'message': f'Pilot with ID {pilot_id} not found'
            }, 404)
        
        pilot_dict = row_to_dict(pilot_data, PILOT_COLUMNS)
        return format_response({'pilot': pilot_dict}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve pilot: {str(e)}'
        }, 500)

@app.route('/api/pilots', methods=['POST'])
def create_pilot():
    # Create a new pilot
    try:
        data = request.get_json()
        
        if not data:
            return format_response({
                'status': 'error',
                'message': 'No data provided'
            }, 400)
        
        # Validate input
        is_valid, error_message = validate_pilot_data(data, is_update=False)
        if not is_valid:
            return format_response({
                'status': 'error',
                'message': error_message
            }, 400)
        
        # Create pilot
        pilot_id = pilot.create(mysql, data)
        
        # Retrieve and return the created pilot
        created_pilot = pilot.get_by_id(mysql, pilot_id)
        pilot_dict = row_to_dict(created_pilot, PILOT_COLUMNS)
        
        return format_response({
            'status': 'success',
            'message': 'Pilot created successfully',
            'pilot': pilot_dict
        }, 201)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to create pilot: {str(e)}'
        }, 500)

@app.route('/api/pilots/<int:pilot_id>', methods=['PUT'])
def update_pilot(pilot_id):
    # Update an existing pilot
    try:
        data = request.get_json()
        
        if not data:
            return format_response({
                'status': 'error',
                'message': 'No data provided'
            }, 400)
        
        # Validate input
        is_valid, error_message = validate_pilot_data(data, is_update=True)
        if not is_valid:
            return format_response({
                'status': 'error',
                'message': error_message
            }, 400)
        
        # Check if pilot exists
        existing_pilot = pilot.get_by_id(mysql, pilot_id)
        if existing_pilot is None:
            return format_response({
                'status': 'error',
                'message': f'Pilot with ID {pilot_id} not found'
            }, 404)
        
        # Update pilot
        pilot.update(mysql, pilot_id, data)
        
        # Retrieve and return updated pilot
        updated_pilot = pilot.get_by_id(mysql, pilot_id)
        pilot_dict = row_to_dict(updated_pilot, PILOT_COLUMNS)
        
        return format_response({
            'status': 'success',
            'message': 'Pilot updated successfully',
            'pilot': pilot_dict
        }, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to update pilot: {str(e)}'
        }, 500)

@app.route('/api/pilots/<int:pilot_id>', methods=['DELETE'])
def delete_pilot(pilot_id):
    # Delete a pilot
    try:
        # Check if pilot exists
        existing_pilot = pilot.get_by_id(mysql, pilot_id)
        if existing_pilot is None:
            return format_response({
                'status': 'error',
                'message': f'Pilot with ID {pilot_id} not found'
            }, 404)
        
        # Delete pilot
        pilot.delete(mysql, pilot_id)
        
        return format_response({
            'status': 'success',
            'message': f'Pilot with ID {pilot_id} deleted successfully'
        }, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to delete pilot: {str(e)}'
        }, 500)

# Ship Endpoints
@app.route('/api/ships', methods=['GET'])
def get_ships():
    # Get all ships or search with criteria
    try:
        # Check for search parameters
        criteria = {}
        
        # Name search (string)
        if request.args.get('name'):
            criteria['name'] = request.args.get('name')
        
        # Ship class ID (numeric)
        if request.args.get('ship_class_id'):
            try:
                criteria['ship_class_id'] = int(request.args.get('ship_class_id'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'ship_class_id must be a valid integer'
                }, 400)
        
        # Pilot ID (numeric)
        if request.args.get('pilot_id'):
            try:
                criteria['pilot_id'] = int(request.args.get('pilot_id'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'pilot_id must be a valid integer'
                }, 400)
        
        # Capacity range (numeric)
        if request.args.get('min_capacity'):
            try:
                criteria['min_capacity'] = int(request.args.get('min_capacity'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'min_capacity must be a valid integer'
                }, 400)
        if request.args.get('max_capacity'):
            try:
                criteria['max_capacity'] = int(request.args.get('max_capacity'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'max_capacity must be a valid integer'
                }, 400)
        
        # Speed range (numeric)
        if request.args.get('min_speed'):
            try:
                criteria['min_speed'] = int(request.args.get('min_speed'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'min_speed must be a valid integer'
                }, 400)
        if request.args.get('max_speed'):
            try:
                criteria['max_speed'] = int(request.args.get('max_speed'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'max_speed must be a valid integer'
                }, 400)
        
        # Shield range (numeric)
        if request.args.get('min_shield'):
            try:
                criteria['min_shield'] = int(request.args.get('min_shield'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'min_shield must be a valid integer'
                }, 400)
        if request.args.get('max_shield'):
            try:
                criteria['max_shield'] = int(request.args.get('max_shield'))
            except ValueError:
                return format_response({
                    'status': 'error',
                    'message': 'max_shield must be a valid integer'
                }, 400)
        
        # Use search if criteria provided, otherwise get all
        if criteria:
            ships_data = ship.search(mysql, criteria)
        else:
            ships_data = ship.get_all(mysql)
        
        ships_list = rows_to_dict_list(ships_data, SHIP_COLUMNS)
        return format_response({'ships': ships_list}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve ships: {str(e)}'
        }, 500)

@app.route('/api/ships/<int:ship_id>', methods=['GET'])
def get_ship(ship_id):
    # Get a single ship by ID
    try:
        ship_data = ship.get_by_id(mysql, ship_id)
        if ship_data is None:
            return format_response({
                'status': 'error',
                'message': f'Ship with ID {ship_id} not found'
            }, 404)
        
        ship_dict = row_to_dict(ship_data, SHIP_COLUMNS)
        return format_response({'ship': ship_dict}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve ship: {str(e)}'
        }, 500)

@app.route('/api/ships', methods=['POST'])
def create_ship():
    # Create a new ship
    try:
        data = request.get_json()
        
        if not data:
            return format_response({
                'status': 'error',
                'message': 'No data provided'
            }, 400)
        
        # Validate input
        is_valid, error_message = validate_ship_data(data, is_update=False)
        if not is_valid:
            return format_response({
                'status': 'error',
                'message': error_message
            }, 400)
        
        # Create ship
        ship_id = ship.create(mysql, data)
        
        # Retrieve and return the created ship
        created_ship = ship.get_by_id(mysql, ship_id)
        ship_dict = row_to_dict(created_ship, SHIP_COLUMNS)
        
        return format_response({
            'status': 'success',
            'message': 'Ship created successfully',
            'ship': ship_dict
        }, 201)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to create ship: {str(e)}'
        }, 500)

@app.route('/api/ships/<int:ship_id>', methods=['PUT'])
def update_ship(ship_id):
    # Update an existing ship
    try:
        data = request.get_json()
        
        if not data:
            return format_response({
                'status': 'error',
                'message': 'No data provided'
            }, 400)
        
        # Validate input
        is_valid, error_message = validate_ship_data(data, is_update=True)
        if not is_valid:
            return format_response({
                'status': 'error',
                'message': error_message
            }, 400)
        
        # Check if ship exists
        existing_ship = ship.get_by_id(mysql, ship_id)
        if existing_ship is None:
            return format_response({
                'status': 'error',
                'message': f'Ship with ID {ship_id} not found'
            }, 404)
        
        # Update ship
        ship.update(mysql, ship_id, data)
        
        # Retrieve and return updated ship
        updated_ship = ship.get_by_id(mysql, ship_id)
        ship_dict = row_to_dict(updated_ship, SHIP_COLUMNS)
        
        return format_response({
            'status': 'success',
            'message': 'Ship updated successfully',
            'ship': ship_dict
        }, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to update ship: {str(e)}'
        }, 500)

@app.route('/api/ships/<int:ship_id>', methods=['DELETE'])
def delete_ship(ship_id):
    # Delete a ship
    try:
        # Check if ship exists
        existing_ship = ship.get_by_id(mysql, ship_id)
        if existing_ship is None:
            return format_response({
                'status': 'error',
                'message': f'Ship with ID {ship_id} not found'
            }, 404)
        
        # Delete ship (also deletes ship_weapons entries)
        ship.delete(mysql, ship_id)
        
        return format_response({
            'status': 'success',
            'message': f'Ship with ID {ship_id} deleted successfully'
        }, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to delete ship: {str(e)}'
        }, 500)

# ShipClass Endpoints
@app.route('/api/ship-classes', methods=['GET'])
def get_ship_classes():
    # Get all ship classes or search with criteria
    try:
        # Check for search parameters
        criteria = {}
        
        # Name search (string)
        if request.args.get('name'):
            criteria['name'] = request.args.get('name')
        
        # Description search (string)
        if request.args.get('description'):
            criteria['description'] = request.args.get('description')
        
        # Use search if criteria provided, otherwise get all
        if criteria:
            ship_classes_data = ship_class.search(mysql, criteria)
        else:
            ship_classes_data = ship_class.get_all(mysql)
        
        ship_classes_list = rows_to_dict_list(ship_classes_data, SHIP_CLASS_COLUMNS)
        return format_response({'ship_classes': ship_classes_list}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve ship classes: {str(e)}'
        }, 500)

@app.route('/api/ship-classes/<int:class_id>', methods=['GET'])
def get_ship_class(class_id):
    # Get a single ship class by ID
    try:
        ship_class_data = ship_class.get_by_id(mysql, class_id)
        if ship_class_data is None:
            return format_response({
                'status': 'error',
                'message': f'Ship class with ID {class_id} not found'
            }, 404)
        
        ship_class_dict = row_to_dict(ship_class_data, SHIP_CLASS_COLUMNS)
        return format_response({'ship_class': ship_class_dict}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve ship class: {str(e)}'
        }, 500)

@app.route('/api/ship-classes', methods=['POST'])
def create_ship_class():
    # Create a new ship class
    try:
        data = request.get_json()
        
        if not data:
            return format_response({
                'status': 'error',
                'message': 'No data provided'
            }, 400)
        
        # Validate input
        is_valid, error_message = validate_ship_class_data(data, is_update=False)
        if not is_valid:
            return format_response({
                'status': 'error',
                'message': error_message
            }, 400)
        
        # Create ship class
        class_id = ship_class.create(mysql, data)
        
        # Retrieve and return the created ship class
        created_ship_class = ship_class.get_by_id(mysql, class_id)
        ship_class_dict = row_to_dict(created_ship_class, SHIP_CLASS_COLUMNS)
        
        return format_response({
            'status': 'success',
            'message': 'Ship class created successfully',
            'ship_class': ship_class_dict
        }, 201)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to create ship class: {str(e)}'
        }, 500)

@app.route('/api/ship-classes/<int:class_id>', methods=['PUT'])
def update_ship_class(class_id):
    # Update an existing ship class
    try:
        data = request.get_json()
        
        if not data:
            return format_response({
                'status': 'error',
                'message': 'No data provided'
            }, 400)
        
        # Validate input
        is_valid, error_message = validate_ship_class_data(data, is_update=True)
        if not is_valid:
            return format_response({
                'status': 'error',
                'message': error_message
            }, 400)
        
        # Check if ship class exists
        existing_ship_class = ship_class.get_by_id(mysql, class_id)
        if existing_ship_class is None:
            return format_response({
                'status': 'error',
                'message': f'Ship class with ID {class_id} not found'
            }, 404)
        
        # Update ship class
        ship_class.update(mysql, class_id, data)
        
        # Retrieve and return updated ship class
        updated_ship_class = ship_class.get_by_id(mysql, class_id)
        ship_class_dict = row_to_dict(updated_ship_class, SHIP_CLASS_COLUMNS)
        
        return format_response({
            'status': 'success',
            'message': 'Ship class updated successfully',
            'ship_class': ship_class_dict
        }, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to update ship class: {str(e)}'
        }, 500)

@app.route('/api/ship-classes/<int:class_id>', methods=['DELETE'])
def delete_ship_class(class_id):
    # Delete a ship class
    try:
        # Check if ship class exists
        existing_ship_class = ship_class.get_by_id(mysql, class_id)
        if existing_ship_class is None:
            return format_response({
                'status': 'error',
                'message': f'Ship class with ID {class_id} not found'
            }, 404)
        
        # Delete ship class
        ship_class.delete(mysql, class_id)
        
        return format_response({
            'status': 'success',
            'message': f'Ship class with ID {class_id} deleted successfully'
        }, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to delete ship class: {str(e)}'
        }, 500)

# WeaponClass Endpoints
@app.route('/api/weapon-classes', methods=['GET'])
def get_weapon_classes():
    # Get all weapon classes
    try:
        weapon_classes_data = weapon_class.get_all(mysql)
        weapon_classes_list = rows_to_dict_list(weapon_classes_data, WEAPON_CLASS_COLUMNS)
        return format_response({'weapon_classes': weapon_classes_list}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve weapon classes: {str(e)}'
        }, 500)

@app.route('/api/weapon-classes/<int:weapon_id>', methods=['GET'])
def get_weapon_class(weapon_id):
    # Get a single weapon class by ID
    try:
        weapon_class_data = weapon_class.get_by_id(mysql, weapon_id)
        if weapon_class_data is None:
            return format_response({
                'status': 'error',
                'message': f'Weapon class with ID {weapon_id} not found'
            }, 404)
        
        weapon_class_dict = row_to_dict(weapon_class_data, WEAPON_CLASS_COLUMNS)
        return format_response({'weapon_class': weapon_class_dict}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve weapon class: {str(e)}'
        }, 500)

@app.route('/api/weapon-classes', methods=['POST'])
def create_weapon_class():
    # Create a new weapon class
    try:
        data = request.get_json()
        
        if not data:
            return format_response({
                'status': 'error',
                'message': 'No data provided'
            }, 400)
        
        # Validate input
        is_valid, error_message = validate_weapon_class_data(data, is_update=False)
        if not is_valid:
            return format_response({
                'status': 'error',
                'message': error_message
            }, 400)
        
        # Create weapon class
        weapon_id = weapon_class.create(mysql, data)
        
        # Retrieve and return the created weapon class
        created_weapon_class = weapon_class.get_by_id(mysql, weapon_id)
        weapon_class_dict = row_to_dict(created_weapon_class, WEAPON_CLASS_COLUMNS)
        
        return format_response({
            'status': 'success',
            'message': 'Weapon class created successfully',
            'weapon_class': weapon_class_dict
        }, 201)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to create weapon class: {str(e)}'
        }, 500)

@app.route('/api/weapon-classes/<int:weapon_id>', methods=['PUT'])
def update_weapon_class(weapon_id):
    # Update an existing weapon class
    try:
        data = request.get_json()
        
        if not data:
            return format_response({
                'status': 'error',
                'message': 'No data provided'
            }, 400)
        
        # Validate input
        is_valid, error_message = validate_weapon_class_data(data, is_update=True)
        if not is_valid:
            return format_response({
                'status': 'error',
                'message': error_message
            }, 400)
        
        # Check if weapon class exists
        existing_weapon_class = weapon_class.get_by_id(mysql, weapon_id)
        if existing_weapon_class is None:
            return format_response({
                'status': 'error',
                'message': f'Weapon class with ID {weapon_id} not found'
            }, 404)
        
        # Update weapon class
        weapon_class.update(mysql, weapon_id, data)
        
        # Retrieve and return updated weapon class
        updated_weapon_class = weapon_class.get_by_id(mysql, weapon_id)
        weapon_class_dict = row_to_dict(updated_weapon_class, WEAPON_CLASS_COLUMNS)
        
        return format_response({
            'status': 'success',
            'message': 'Weapon class updated successfully',
            'weapon_class': weapon_class_dict
        }, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to update weapon class: {str(e)}'
        }, 500)

@app.route('/api/weapon-classes/<int:weapon_id>', methods=['DELETE'])
def delete_weapon_class(weapon_id):
    # Delete a weapon class
    try:
        # Check if weapon class exists
        existing_weapon_class = weapon_class.get_by_id(mysql, weapon_id)
        if existing_weapon_class is None:
            return format_response({
                'status': 'error',
                'message': f'Weapon class with ID {weapon_id} not found'
            }, 404)
        
        # Delete weapon class
        weapon_class.delete(mysql, weapon_id)
        
        return format_response({
            'status': 'success',
            'message': f'Weapon class with ID {weapon_id} deleted successfully'
        }, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to delete weapon class: {str(e)}'
        }, 500)

# ShipWeapons Endpoints
@app.route('/api/ship-weapons', methods=['GET'])
def get_ship_weapons():
    # Get all ship weapon assignments
    try:
        ship_weapons_data = ship_weapons.get_all(mysql)
        ship_weapons_list = rows_to_dict_list(ship_weapons_data, SHIP_WEAPONS_COLUMNS)
        return format_response({'ship_weapons': ship_weapons_list}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve ship weapons: {str(e)}'
        }, 500)

@app.route('/api/ship-weapons/ship/<int:ship_id>', methods=['GET'])
def get_ship_weapons_by_ship(ship_id):
    # Get all weapons for a specific ship
    try:
        ship_weapons_data = ship_weapons.get_by_ship_id(mysql, ship_id)
        ship_weapons_list = rows_to_dict_list(ship_weapons_data, SHIP_WEAPONS_COLUMNS)
        return format_response({'ship_weapons': ship_weapons_list}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve ship weapons: {str(e)}'
        }, 500)

@app.route('/api/ship-weapons/<int:ship_id>/<int:ship_class_id>/<int:weapon_class_id>', methods=['GET'])
def get_ship_weapon(ship_id, ship_class_id, weapon_class_id):
    # Get a specific ship weapon assignment
    try:
        ship_weapon_data = ship_weapons.get_by_id(mysql, ship_id, ship_class_id, weapon_class_id)
        if ship_weapon_data is None:
            return format_response({
                'status': 'error',
                'message': f'Ship weapon assignment not found'
            }, 404)
        
        ship_weapon_dict = row_to_dict(ship_weapon_data, SHIP_WEAPONS_COLUMNS)
        return format_response({'ship_weapon': ship_weapon_dict}, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to retrieve ship weapon: {str(e)}'
        }, 500)

@app.route('/api/ship-weapons', methods=['POST'])
def create_ship_weapon():
    # Create a new ship weapon assignment
    try:
        data = request.get_json()
        
        if not data:
            return format_response({
                'status': 'error',
                'message': 'No data provided'
            }, 400)
        
        # Validate required fields
        required_fields = ['ship_id', 'ship_class_id', 'weapon_class_id', 'name']
        for field in required_fields:
            if field not in data:
                return format_response({
                    'status': 'error',
                    'message': f'Missing required field: {field}'
                }, 400)
        
        # Validate data types
        if not isinstance(data['ship_id'], int) or data['ship_id'] < 1:
            return format_response({
                'status': 'error',
                'message': 'Field ship_id must be a positive integer'
            }, 400)
        
        if not isinstance(data['ship_class_id'], int) or data['ship_class_id'] < 1:
            return format_response({
                'status': 'error',
                'message': 'Field ship_class_id must be a positive integer'
            }, 400)
        
        if not isinstance(data['weapon_class_id'], int) or data['weapon_class_id'] < 1:
            return format_response({
                'status': 'error',
                'message': 'Field weapon_class_id must be a positive integer'
            }, 400)
        
        if not isinstance(data['name'], str) or len(data['name'].strip()) == 0:
            return format_response({
                'status': 'error',
                'message': 'Field name must be a non-empty string'
            }, 400)
        
        # Create ship weapon assignment
        ship_weapons.create(mysql, data)
        
        # Retrieve and return the created assignment
        created_ship_weapon = ship_weapons.get_by_id(mysql, data['ship_id'], 
                                                     data['ship_class_id'], 
                                                     data['weapon_class_id'])
        ship_weapon_dict = row_to_dict(created_ship_weapon, SHIP_WEAPONS_COLUMNS)
        
        return format_response({
            'status': 'success',
            'message': 'Ship weapon assignment created successfully',
            'ship_weapon': ship_weapon_dict
        }, 201)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to create ship weapon assignment: {str(e)}'
        }, 500)

@app.route('/api/ship-weapons/<int:ship_id>/<int:ship_class_id>/<int:weapon_class_id>', methods=['DELETE'])
def delete_ship_weapon(ship_id, ship_class_id, weapon_class_id):
    # Delete a ship weapon assignment
    try:
        # Check if assignment exists
        existing_ship_weapon = ship_weapons.get_by_id(mysql, ship_id, ship_class_id, weapon_class_id)
        if existing_ship_weapon is None:
            return format_response({
                'status': 'error',
                'message': f'Ship weapon assignment not found'
            }, 404)
        
        # Delete ship weapon assignment
        ship_weapons.delete(mysql, ship_id, ship_class_id, weapon_class_id)
        
        return format_response({
            'status': 'success',
            'message': f'Ship weapon assignment deleted successfully'
        }, 200)
    except Exception as e:
        return format_response({
            'status': 'error',
            'message': f'Failed to delete ship weapon assignment: {str(e)}'
        }, 500)

# Error Handlers
@app.errorhandler(404)
def not_found(error):
    # Handle 404 - Resource not found
    return format_response({
        'status': 'error',
        'message': 'Endpoint not found',
        'error': str(error)
    }, 404)

@app.errorhandler(405)
def method_not_allowed(error):
    #Handle 405 - Method not allowed
    return format_response({
        'status': 'error',
        'message': 'Method not allowed',
        'error': str(error)
    }, 405)

@app.errorhandler(500)
def internal_error(error):
    #Handle 500 - Internal server error
    return format_response({
        'status': 'error',
        'message': 'Internal server error',
        'error': str(error)
    }, 500)

if __name__ == '__main__':
    app.run(debug=True)
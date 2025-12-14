import json
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from utils.formatters import format_response, row_to_dict, rows_to_dict_list
from utils.validators import validate_pilot_data, validate_ship_data
from models import pilot, ship

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
    # Get all pilots
    try:
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
    # Get all ships
    try:
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
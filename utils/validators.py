"""
Input validation utilities for all entities
"""


def validate_pilot_data(data, is_update=False):
    # Validate pilot data for create or update operations.

    # Required fields for creation
    required_fields = ['name', 'flight_years', 'rank', 'mission_success']
    
    # Check required fields only for creation
    if not is_update:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
    
    # Validate name if provided
    if 'name' in data:
        if not isinstance(data['name'], str):
            return False, "Field 'name' must be a string"
        if len(data['name'].strip()) == 0:
            return False, "Field 'name' cannot be empty"
        if len(data['name']) > 100:
            return False, "Field 'name' cannot exceed 100 characters"
    
    # Validate flight_years if provided
    if 'flight_years' in data:
        if not isinstance(data['flight_years'], int):
            return False, "Field 'flight_years' must be an integer"
        if data['flight_years'] < 0:
            return False, "Field 'flight_years' cannot be negative"
    
    # Validate rank if provided
    if 'rank' in data:
        if not isinstance(data['rank'], str):
            return False, "Field 'rank' must be a string"
        if len(data['rank'].strip()) == 0:
            return False, "Field 'rank' cannot be empty"
        if len(data['rank']) > 50:
            return False, "Field 'rank' cannot exceed 50 characters"
    
    # Validate mission_success if provided
    if 'mission_success' in data:
        if not isinstance(data['mission_success'], int):
            return False, "Field 'mission_success' must be an integer"
        if data['mission_success'] < 0:
            return False, "Field 'mission_success' cannot be negative"
    
    return True, None


def validate_ship_data(data, is_update=False):

    # Validate ship data for create or update operations.
   
    # Required fields for creation
    required_fields = ['name', 'capacity', 'speed', 'shield', 'ship_class_id', 'pilot_id']
    
    # Check required fields only for creation
    if not is_update:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
    
    # Validate name if provided
    if 'name' in data:
        if not isinstance(data['name'], str):
            return False, "Field 'name' must be a string"
        if len(data['name'].strip()) == 0:
            return False, "Field 'name' cannot be empty"
        if len(data['name']) > 100:
            return False, "Field 'name' cannot exceed 100 characters"
    
    # Validate capacity if provided
    if 'capacity' in data:
        if not isinstance(data['capacity'], int):
            return False, "Field 'capacity' must be an integer"
        if data['capacity'] < 0:
            return False, "Field 'capacity' cannot be negative"
    
    # Validate speed if provided
    if 'speed' in data:
        if not isinstance(data['speed'], int):
            return False, "Field 'speed' must be an integer"
        if data['speed'] < 0:
            return False, "Field 'speed' cannot be negative"
    
    # Validate shield if provided
    if 'shield' in data:
        if not isinstance(data['shield'], int):
            return False, "Field 'shield' must be an integer"
        if data['shield'] < 0:
            return False, "Field 'shield' cannot be negative"
    
    # Validate ship_class_id if provided
    if 'ship_class_id' in data:
        if not isinstance(data['ship_class_id'], int):
            return False, "Field 'ship_class_id' must be an integer"
        if data['ship_class_id'] < 1:
            return False, "Field 'ship_class_id' must be a positive integer"
    
    # Validate pilot_id if provided
    if 'pilot_id' in data:
        if not isinstance(data['pilot_id'], int):
            return False, "Field 'pilot_id' must be an integer"
        if data['pilot_id'] < 1:
            return False, "Field 'pilot_id' must be a positive integer"
    
    return True, None


def validate_ship_class_data(data, is_update=False):

    # Validate ship class data for create or update operations.

    # Required fields for creation (description is optional)
    required_fields = ['name']
    
    # Check required fields only for creation
    if not is_update:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
    
    # Validate name if provided
    if 'name' in data:
        if not isinstance(data['name'], str):
            return False, "Field 'name' must be a string"
        if len(data['name'].strip()) == 0:
            return False, "Field 'name' cannot be empty"
        if len(data['name']) > 100:
            return False, "Field 'name' cannot exceed 100 characters"
    
    # Validate description if provided (optional field)
    if 'description' in data:
        if data['description'] is not None:
            if not isinstance(data['description'], str):
                return False, "Field 'description' must be a string"
            if len(data['description']) > 500:
                return False, "Field 'description' cannot exceed 500 characters"
    
    return True, None


def validate_weapon_class_data(data, is_update=False):

    # Validate weapon class data for create or update operations.

    # Required fields for creation
    required_fields = ['class', 'damage', 'reload_speed', 'spread', 'range']
    
    # Check required fields only for creation
    if not is_update:
        for field in required_fields:
            if field not in data:
                return False, f"Missing required field: {field}"
    
    # Validate class if provided
    if 'class' in data:
        if not isinstance(data['class'], str):
            return False, "Field 'class' must be a string"
        if len(data['class'].strip()) == 0:
            return False, "Field 'class' cannot be empty"
        if len(data['class']) > 50:
            return False, "Field 'class' cannot exceed 50 characters"
    
    # Validate damage if provided
    if 'damage' in data:
        if not isinstance(data['damage'], int):
            return False, "Field 'damage' must be an integer"
        if data['damage'] < 0:
            return False, "Field 'damage' cannot be negative"
    
    # Validate reload_speed if provided
    if 'reload_speed' in data:
        if not isinstance(data['reload_speed'], int):
            return False, "Field 'reload_speed' must be an integer"
        if data['reload_speed'] < 0:
            return False, "Field 'reload_speed' cannot be negative"
    
    # Validate spread if provided
    if 'spread' in data:
        if not isinstance(data['spread'], int):
            return False, "Field 'spread' must be an integer"
        if data['spread'] < 0:
            return False, "Field 'spread' cannot be negative"
    
    # Validate range if provided
    if 'range' in data:
        if not isinstance(data['range'], int):
            return False, "Field 'range' must be an integer"
        if data['range'] < 0:
            return False, "Field 'range' cannot be negative"
    
    return True, None

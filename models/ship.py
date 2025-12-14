def get_all(mysql):
    # Get all ships with JOINs to pilot and ship_class
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT s.id, s.name, s.capacity, s.speed, s.shield, 
               s.ship_class_id, sc.name as ship_class_name,
               s.pilot_id, p.name as pilot_name
        FROM ship s
        LEFT JOIN ship_class sc ON s.ship_class_id = sc.id
        LEFT JOIN pilot p ON s.pilot_id = p.id
        ORDER BY s.id
    ''')
    ships = cursor.fetchall()
    cursor.close()
    return ships


def get_by_id(mysql, ship_id):
    # Get a specific ship by ID with JOINs
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT s.id, s.name, s.capacity, s.speed, s.shield, 
               s.ship_class_id, sc.name as ship_class_name,
               s.pilot_id, p.name as pilot_name
        FROM ship s
        LEFT JOIN ship_class sc ON s.ship_class_id = sc.id
        LEFT JOIN pilot p ON s.pilot_id = p.id
        WHERE s.id = %s
    ''', (ship_id,))
    ship = cursor.fetchone()
    cursor.close()
    return ship


def create(mysql, data):
    # Create a new ship
    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO ship (name, capacity, speed, shield, ship_class_id, pilot_id)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (data['name'], data['capacity'], data['speed'], 
          data['shield'], data['ship_class_id'], data['pilot_id']))
    mysql.connection.commit()
    ship_id = cursor.lastrowid
    cursor.close()
    return ship_id


def update(mysql, ship_id, data):
    # Update an existing ship
    update_fields = []
    values = []
    
    if 'name' in data:
        update_fields.append('name = %s')
        values.append(data['name'])
    
    if 'capacity' in data:
        update_fields.append('capacity = %s')
        values.append(data['capacity'])
    
    if 'speed' in data:
        update_fields.append('speed = %s')
        values.append(data['speed'])
    
    if 'shield' in data:
        update_fields.append('shield = %s')
        values.append(data['shield'])
    
    if 'ship_class_id' in data:
        update_fields.append('ship_class_id = %s')
        values.append(data['ship_class_id'])
    
    if 'pilot_id' in data:
        update_fields.append('pilot_id = %s')
        values.append(data['pilot_id'])
    
    values.append(ship_id)
    
    cursor = mysql.connection.cursor()
    query = f"UPDATE ship SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(query, values)
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected


def delete(mysql, ship_id):
    # Delete a ship (must delete ship_weapons entries first)
    cursor = mysql.connection.cursor()
    
    # First delete related ship_weapons entries
    cursor.execute('DELETE FROM ship_weapons WHERE ship_id = %s', (ship_id,))
    
    # Then delete the ship
    cursor.execute('DELETE FROM ship WHERE id = %s', (ship_id,))
    
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected


def search(mysql, criteria):
    # Search ships based on criteria
    cursor = mysql.connection.cursor()
    
    # Build dynamic WHERE clause
    where_clauses = []
    values = []
    
    # Name search (LIKE - partial match)
    if 'name' in criteria and criteria['name']:
        where_clauses.append('s.name LIKE %s')
        values.append(f"%{criteria['name']}%")
    
    # Ship class ID (exact match)
    if 'ship_class_id' in criteria and criteria['ship_class_id'] is not None:
        where_clauses.append('s.ship_class_id = %s')
        values.append(criteria['ship_class_id'])
    
    # Pilot ID (exact match)
    if 'pilot_id' in criteria and criteria['pilot_id'] is not None:
        where_clauses.append('s.pilot_id = %s')
        values.append(criteria['pilot_id'])
    
    # Capacity range
    if 'min_capacity' in criteria and criteria['min_capacity'] is not None:
        where_clauses.append('s.capacity >= %s')
        values.append(criteria['min_capacity'])
    if 'max_capacity' in criteria and criteria['max_capacity'] is not None:
        where_clauses.append('s.capacity <= %s')
        values.append(criteria['max_capacity'])
    
    # Speed range
    if 'min_speed' in criteria and criteria['min_speed'] is not None:
        where_clauses.append('s.speed >= %s')
        values.append(criteria['min_speed'])
    if 'max_speed' in criteria and criteria['max_speed'] is not None:
        where_clauses.append('s.speed <= %s')
        values.append(criteria['max_speed'])
    
    # Shield range
    if 'min_shield' in criteria and criteria['min_shield'] is not None:
        where_clauses.append('s.shield >= %s')
        values.append(criteria['min_shield'])
    if 'max_shield' in criteria and criteria['max_shield'] is not None:
        where_clauses.append('s.shield <= %s')
        values.append(criteria['max_shield'])
    
    # Build query
    query = '''
        SELECT s.id, s.name, s.capacity, s.speed, s.shield, 
               s.ship_class_id, sc.name as ship_class_name,
               s.pilot_id, p.name as pilot_name
        FROM ship s
        LEFT JOIN ship_class sc ON s.ship_class_id = sc.id
        LEFT JOIN pilot p ON s.pilot_id = p.id
    '''
    
    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)
    query += ' ORDER BY s.id'
    
    cursor.execute(query, values)
    ships = cursor.fetchall()
    cursor.close()
    return ships

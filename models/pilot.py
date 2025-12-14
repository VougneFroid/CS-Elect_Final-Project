def get_all(mysql):
    # Get all pilots from the database
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT id, name, flight_years, `rank`, mission_success 
        FROM pilot
        ORDER BY id
    ''')
    pilots = cursor.fetchall()
    cursor.close()
    return pilots


def get_by_id(mysql, pilot_id):
    # Get a specific pilot by ID
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT id, name, flight_years, `rank`, mission_success 
        FROM pilot 
        WHERE id = %s
    ''', (pilot_id,))
    pilot = cursor.fetchone()
    cursor.close()
    return pilot


def create(mysql, data):
    # Create a new pilot
    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO pilot (name, flight_years, `rank`, mission_success)
        VALUES (%s, %s, %s, %s)
    ''', (data['name'], data['flight_years'], data['rank'], data['mission_success']))
    mysql.connection.commit()
    pilot_id = cursor.lastrowid
    cursor.close()
    return pilot_id


def update(mysql, pilot_id, data):
    # Update an existing pilot
    update_fields = []
    values = []
    
    if 'name' in data:
        update_fields.append('name = %s')
        values.append(data['name'])
    
    if 'flight_years' in data:
        update_fields.append('flight_years = %s')
        values.append(data['flight_years'])
    
    if 'rank' in data:
        update_fields.append('`rank` = %s')
        values.append(data['rank'])
    
    if 'mission_success' in data:
        update_fields.append('mission_success = %s')
        values.append(data['mission_success'])
    
    values.append(pilot_id)
    
    cursor = mysql.connection.cursor()
    query = f"UPDATE pilot SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(query, values)
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected


def delete(mysql, pilot_id):
    # Delete a pilot
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM pilot WHERE id = %s', (pilot_id,))
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected


def search(mysql, criteria):
    # Search pilots based on criteria
    cursor = mysql.connection.cursor()
    
    # Build dynamic WHERE clause
    where_clauses = []
    values = []
    
    # Name search (LIKE - partial match)
    if 'name' in criteria and criteria['name']:
        where_clauses.append('name LIKE %s')
        values.append(f"%{criteria['name']}%")
    
    # Rank search (exact match)
    if 'rank' in criteria and criteria['rank']:
        where_clauses.append('`rank` = %s')
        values.append(criteria['rank'])
    
    # Minimum flight years
    if 'min_flight_years' in criteria and criteria['min_flight_years'] is not None:
        where_clauses.append('flight_years >= %s')
        values.append(criteria['min_flight_years'])
    
    # Minimum mission success
    if 'min_mission_success' in criteria and criteria['min_mission_success'] is not None:
        where_clauses.append('mission_success >= %s')
        values.append(criteria['min_mission_success'])
    
    # Build query
    query = 'SELECT id, name, flight_years, `rank`, mission_success FROM pilot'
    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)
    query += ' ORDER BY id'
    
    # Execute with or without values
    if values:
        cursor.execute(query, values)
    else:
        cursor.execute(query)
    
    pilots = cursor.fetchall()
    cursor.close()
    return pilots

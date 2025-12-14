def get_all(mysql):
    # Get all ship classes from the database
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT id, name, description
        FROM ship_class
        ORDER BY id
    ''')
    ship_classes = cursor.fetchall()
    cursor.close()
    return ship_classes


def get_by_id(mysql, class_id):
    # Get a specific ship class by ID
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT id, name, description
        FROM ship_class
        WHERE id = %s
    ''', (class_id,))
    ship_class = cursor.fetchone()
    cursor.close()
    return ship_class


def create(mysql, data):
    # Create a new ship class (description is optional)
    cursor = mysql.connection.cursor()
    
    # Handle optional description field
    description = data.get('description', None)
    
    cursor.execute('''
        INSERT INTO ship_class (name, description)
        VALUES (%s, %s)
    ''', (data['name'], description))
    mysql.connection.commit()
    class_id = cursor.lastrowid
    cursor.close()
    return class_id


def update(mysql, class_id, data):
    # Update an existing ship class
    update_fields = []
    values = []
    
    if 'name' in data:
        update_fields.append('name = %s')
        values.append(data['name'])
    
    if 'description' in data:
        update_fields.append('description = %s')
        values.append(data['description'])
    
    values.append(class_id)
    
    cursor = mysql.connection.cursor()
    query = f"UPDATE ship_class SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(query, values)
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected


def delete(mysql, class_id):
    # Delete a ship class
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM ship_class WHERE id = %s', (class_id,))
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected


def search(mysql, criteria):
    # Search ship classes based on criteria
    cursor = mysql.connection.cursor()
    
    # Build dynamic WHERE clause
    where_clauses = []
    values = []
    
    # Name search (LIKE - partial match)
    if 'name' in criteria and criteria['name']:
        where_clauses.append('name LIKE %s')
        values.append(f"%{criteria['name']}%")
    
    # Description search (LIKE - partial match)
    if 'description' in criteria and criteria['description']:
        where_clauses.append('description LIKE %s')
        values.append(f"%{criteria['description']}%")
    
    # Build query
    query = 'SELECT id, name, description FROM ship_class'
    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)
    query += ' ORDER BY id'
    
    cursor.execute(query, values)
    ship_classes = cursor.fetchall()
    cursor.close()
    return ship_classes

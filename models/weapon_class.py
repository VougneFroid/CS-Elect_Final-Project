def get_all(mysql):
    # Get all weapon classes from the database
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT id, class, damage, reload_speed, spread, `range`
        FROM weapon_class
        ORDER BY id
    ''')
    weapon_classes = cursor.fetchall()
    cursor.close()
    return weapon_classes


def get_by_id(mysql, weapon_id):
    # Get a specific weapon class by ID
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT id, class, damage, reload_speed, spread, `range`
        FROM weapon_class
        WHERE id = %s
    ''', (weapon_id,))
    weapon_class = cursor.fetchone()
    cursor.close()
    return weapon_class


def create(mysql, data):
    # Create a new weapon class
    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO weapon_class (class, damage, reload_speed, spread, `range`)
        VALUES (%s, %s, %s, %s, %s)
    ''', (data['class'], data['damage'], data['reload_speed'], 
          data['spread'], data['range']))
    mysql.connection.commit()
    weapon_id = cursor.lastrowid
    cursor.close()
    return weapon_id


def update(mysql, weapon_id, data):
    # Update an existing weapon class
    update_fields = []
    values = []
    
    if 'class' in data:
        update_fields.append('class = %s')
        values.append(data['class'])
    
    if 'damage' in data:
        update_fields.append('damage = %s')
        values.append(data['damage'])
    
    if 'reload_speed' in data:
        update_fields.append('reload_speed = %s')
        values.append(data['reload_speed'])
    
    if 'spread' in data:
        update_fields.append('spread = %s')
        values.append(data['spread'])
    
    if 'range' in data:
        update_fields.append('`range` = %s')
        values.append(data['range'])
    
    values.append(weapon_id)
    
    cursor = mysql.connection.cursor()
    query = f"UPDATE weapon_class SET {', '.join(update_fields)} WHERE id = %s"
    cursor.execute(query, values)
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected


def delete(mysql, weapon_id):
    # Delete a weapon class
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM weapon_class WHERE id = %s', (weapon_id,))
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected


def search(mysql, criteria):
    # Search weapon classes based on criteria
    cursor = mysql.connection.cursor()
    
    # Build dynamic WHERE clause
    where_clauses = []
    values = []
    
    # Class name search (LIKE - partial match)
    if 'class' in criteria and criteria['class']:
        where_clauses.append('class LIKE %s')
        values.append(f"%{criteria['class']}%")
    
    # Damage range
    if 'min_damage' in criteria and criteria['min_damage'] is not None:
        where_clauses.append('damage >= %s')
        values.append(criteria['min_damage'])
    if 'max_damage' in criteria and criteria['max_damage'] is not None:
        where_clauses.append('damage <= %s')
        values.append(criteria['max_damage'])
    
    # Reload speed range
    if 'min_reload_speed' in criteria and criteria['min_reload_speed'] is not None:
        where_clauses.append('reload_speed >= %s')
        values.append(criteria['min_reload_speed'])
    if 'max_reload_speed' in criteria and criteria['max_reload_speed'] is not None:
        where_clauses.append('reload_speed <= %s')
        values.append(criteria['max_reload_speed'])
    
    # Spread range
    if 'min_spread' in criteria and criteria['min_spread'] is not None:
        where_clauses.append('spread >= %s')
        values.append(criteria['min_spread'])
    if 'max_spread' in criteria and criteria['max_spread'] is not None:
        where_clauses.append('spread <= %s')
        values.append(criteria['max_spread'])
    
    # Range range
    if 'min_range' in criteria and criteria['min_range'] is not None:
        where_clauses.append('`range` >= %s')
        values.append(criteria['min_range'])
    if 'max_range' in criteria and criteria['max_range'] is not None:
        where_clauses.append('`range` <= %s')
        values.append(criteria['max_range'])
    
    # Build query
    query = 'SELECT id, class, damage, reload_speed, spread, `range` FROM weapon_class'
    if where_clauses:
        query += ' WHERE ' + ' AND '.join(where_clauses)
    query += ' ORDER BY id'
    
    cursor.execute(query, values)
    weapon_classes = cursor.fetchall()
    cursor.close()
    return weapon_classes

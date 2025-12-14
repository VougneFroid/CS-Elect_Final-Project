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

def get_all(mysql):
    # Get all ship weapon assignments with JOINs
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT sw.ship_id, s.name as ship_name,
               sw.ship_class_id, sc.name as ship_class_name,
               sw.weapon_class_id, wc.class as weapon_class_name,
               sw.name
        FROM ship_weapons sw
        LEFT JOIN ship s ON sw.ship_id = s.id
        LEFT JOIN ship_class sc ON sw.ship_class_id = sc.id
        LEFT JOIN weapon_class wc ON sw.weapon_class_id = wc.id
        ORDER BY sw.ship_id, sw.ship_class_id, sw.weapon_class_id
    ''')
    ship_weapons = cursor.fetchall()
    cursor.close()
    return ship_weapons


def get_by_ship_id(mysql, ship_id):
    # Get all weapons for a specific ship
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT sw.ship_id, s.name as ship_name,
               sw.ship_class_id, sc.name as ship_class_name,
               sw.weapon_class_id, wc.class as weapon_class_name,
               sw.name
        FROM ship_weapons sw
        LEFT JOIN ship s ON sw.ship_id = s.id
        LEFT JOIN ship_class sc ON sw.ship_class_id = sc.id
        LEFT JOIN weapon_class wc ON sw.weapon_class_id = wc.id
        WHERE sw.ship_id = %s
        ORDER BY sw.ship_class_id, sw.weapon_class_id
    ''', (ship_id,))
    ship_weapons = cursor.fetchall()
    cursor.close()
    return ship_weapons


def get_by_id(mysql, ship_id, ship_class_id, weapon_class_id):
    # Get a specific ship weapon assignment by composite key
    cursor = mysql.connection.cursor()
    cursor.execute('''
        SELECT sw.ship_id, s.name as ship_name,
               sw.ship_class_id, sc.name as ship_class_name,
               sw.weapon_class_id, wc.class as weapon_class_name,
               sw.name
        FROM ship_weapons sw
        LEFT JOIN ship s ON sw.ship_id = s.id
        LEFT JOIN ship_class sc ON sw.ship_class_id = sc.id
        LEFT JOIN weapon_class wc ON sw.weapon_class_id = wc.id
        WHERE sw.ship_id = %s 
          AND sw.ship_class_id = %s 
          AND sw.weapon_class_id = %s
    ''', (ship_id, ship_class_id, weapon_class_id))
    ship_weapon = cursor.fetchone()
    cursor.close()
    return ship_weapon


def create(mysql, data):
    # Create a new ship weapon assignment
    cursor = mysql.connection.cursor()
    cursor.execute('''
        INSERT INTO ship_weapons (ship_id, ship_class_id, weapon_class_id, name)
        VALUES (%s, %s, %s, %s)
    ''', (data['ship_id'], data['ship_class_id'], 
          data['weapon_class_id'], data['name']))
    mysql.connection.commit()
    cursor.close()
    return True


def delete(mysql, ship_id, ship_class_id, weapon_class_id):
    # Delete a ship weapon assignment by composite key
    cursor = mysql.connection.cursor()
    cursor.execute('''
        DELETE FROM ship_weapons 
        WHERE ship_id = %s 
          AND ship_class_id = %s 
          AND weapon_class_id = %s
    ''', (ship_id, ship_class_id, weapon_class_id))
    mysql.connection.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected

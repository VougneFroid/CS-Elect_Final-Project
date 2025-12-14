"""
User model for authentication and user management.
"""

def get_all(mysql):
    """Get all users (excluding passwords)"""
    cursor = mysql.connection.cursor()
    query = "SELECT id, username, email, created_at FROM users"
    cursor.execute(query)
    users = cursor.fetchall()
    cursor.close()
    return users

def get_by_id(mysql, user_id):
    """Get a user by ID (excluding password)"""
    cursor = mysql.connection.cursor()
    query = "SELECT id, username, email, created_at FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_by_username(mysql, username):
    """Get a user by username (including password hash for authentication)"""
    cursor = mysql.connection.cursor()
    query = "SELECT id, username, email, password_hash, created_at FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    cursor.close()
    return user

def get_by_email(mysql, email):
    """Get a user by email (excluding password)"""
    cursor = mysql.connection.cursor()
    query = "SELECT id, username, email, created_at FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

def create(mysql, data):
    """
    Create a new user.
    
    Args:
        mysql: MySQL connection
        data: Dictionary containing user data (username, email, password_hash)
        
    Returns:
        int: ID of the created user
    """
    cursor = mysql.connection.cursor()
    query = """
        INSERT INTO users (username, email, password_hash)
        VALUES (%s, %s, %s)
    """
    cursor.execute(query, (
        data['username'],
        data['email'],
        data['password_hash']
    ))
    mysql.connection.commit()
    user_id = cursor.lastrowid
    cursor.close()
    return user_id

def update(mysql, user_id, data):
    """
    Update an existing user.
    
    Args:
        mysql: MySQL connection
        user_id: ID of the user to update
        data: Dictionary containing fields to update
    """
    cursor = mysql.connection.cursor()
    
    # Build dynamic update query
    fields = []
    values = []
    
    if 'username' in data:
        fields.append('username = %s')
        values.append(data['username'])
    
    if 'email' in data:
        fields.append('email = %s')
        values.append(data['email'])
    
    if 'password_hash' in data:
        fields.append('password_hash = %s')
        values.append(data['password_hash'])
    
    if not fields:
        cursor.close()
        return
    
    values.append(user_id)
    query = f"UPDATE users SET {', '.join(fields)} WHERE id = %s"
    
    cursor.execute(query, tuple(values))
    mysql.connection.commit()
    cursor.close()

def delete(mysql, user_id):
    """
    Delete a user.
    
    Args:
        mysql: MySQL connection
        user_id: ID of the user to delete
    """
    cursor = mysql.connection.cursor()
    query = "DELETE FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    mysql.connection.commit()
    cursor.close()

def username_exists(mysql, username):
    """
    Check if a username already exists.
    
    Args:
        mysql: MySQL connection
        username: Username to check
        
    Returns:
        bool: True if username exists, False otherwise
    """
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM users WHERE username = %s"
    cursor.execute(query, (username,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

def email_exists(mysql, email):
    """
    Check if an email already exists.
    
    Args:
        mysql: MySQL connection
        email: Email to check
        
    Returns:
        bool: True if email exists, False otherwise
    """
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    count = cursor.fetchone()[0]
    cursor.close()
    return count > 0

"""
Authentication utilities for JWT token management and password hashing.
"""
import jwt
import datetime
from functools import wraps
from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Secret key for JWT token encoding/decoding
# In production, this should be stored in environment variables
SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-secret-key-change-in-production')
JWT_ALGORITHM = 'HS256'
TOKEN_EXPIRATION_HOURS = 24

def hash_password(password):
    """
    Hash a password using Werkzeug's security functions.
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Hashed password
    """
    return generate_password_hash(password)

def verify_password(password_hash, password):
    """
    Verify a password against its hash.
    
    Args:
        password_hash (str): Hashed password
        password (str): Plain text password to verify
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return check_password_hash(password_hash, password)

def generate_token(user_id, username):
    """
    Generate a JWT token for a user.
    
    Args:
        user_id (int): User's ID
        username (str): User's username
        
    Returns:
        str: JWT token
    """
    payload = {
        'user_id': user_id,
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=TOKEN_EXPIRATION_HOURS),
        'iat': datetime.datetime.utcnow()
    }
    
    token = jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)
    return token

def decode_token(token):
    """
    Decode and validate a JWT token.
    
    Args:
        token (str): JWT token
        
    Returns:
        dict: Decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token

def token_required(f):
    """
    Decorator to protect routes that require authentication.
    
    Usage:
        @app.route('/api/protected')
        @token_required
        def protected_route(current_user):
            return jsonify({'message': 'Access granted', 'user': current_user})
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                # Expected format: "Bearer <token>"
                token = auth_header.split(' ')[1]
            except IndexError:
                return jsonify({
                    'status': 'error',
                    'message': 'Invalid Authorization header format. Use: Bearer <token>'
                }), 401
        
        if not token:
            return jsonify({
                'status': 'error',
                'message': 'Authentication token is missing'
            }), 401
        
        # Decode and validate token
        payload = decode_token(token)
        
        if payload is None:
            return jsonify({
                'status': 'error',
                'message': 'Invalid or expired token'
            }), 401
        
        # Pass the decoded user information to the route
        current_user = {
            'user_id': payload['user_id'],
            'username': payload['username']
        }
        
        return f(current_user, *args, **kwargs)
    
    return decorated

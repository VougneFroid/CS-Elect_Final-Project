import json
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from utils.formatters import format_response

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vondev'
app.config['MYSQL_DB'] = 'shiperd'

mysql = MySQL(app)

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
import json
from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

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

if __name__ == '__main__':
    app.run(debug=True)
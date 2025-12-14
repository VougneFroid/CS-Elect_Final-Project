from flask import Flask
from flask_mysqldb import MySQL

app = Flask('test')
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'vondev'
app.config['MYSQL_DB'] = 'shiperd'

mysql = MySQL(app)

with app.app_context():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT COUNT(*) FROM pilot')
    result = cursor.fetchone()
    cursor.close()
    print(f'Success! Pilot count: {result[0]}')

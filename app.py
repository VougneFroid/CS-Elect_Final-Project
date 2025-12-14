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
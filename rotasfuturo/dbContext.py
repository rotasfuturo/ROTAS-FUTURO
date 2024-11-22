import os
from flask_mysqldb import MySQL

mysql = MySQL()

class DBContext:
    SECRET_KEY = "123"
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'Rot@sfuturo2024'
    MYSQL_DB = 'rotasfuturo'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app/static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

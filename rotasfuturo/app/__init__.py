import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_mysqldb import MySQL
from app.controllers import teste
from dbContext import DBContext, mysql

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DBContext)

    app.register_blueprint(teste.bp)
    mysql.init_app(app)
    return app

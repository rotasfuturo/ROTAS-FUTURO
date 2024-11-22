import os
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from flask_mysqldb import MySQL
from app.controllers import teste, home, aluno, professor, atividade, matricula, turma, visita
from dbContext import DBContext, mysql

mysql = MySQL()

def create_app():
    app = Flask(__name__)
    app.config.from_object(DBContext)

    app.register_blueprint(home.bp)
    app.register_blueprint(teste.bp)
    app.register_blueprint(aluno.bp)
    app.register_blueprint(professor.bp)
    app.register_blueprint(atividade.bp)
    app.register_blueprint(matricula.bp)
    app.register_blueprint(turma.bp)
    app.register_blueprint(visita.bp)
    mysql.init_app(app)
    return app

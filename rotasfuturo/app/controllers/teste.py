from flask import Blueprint, render_template, request, flash
from dbContext import mysql
from app.models.teste import Teste

bp = Blueprint('teste', __name__)

@bp.route('/')
def home():
    return render_template('index.html')

@bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nome = request.form.get('nome').strip(),
        idade = request.form.get('idade').strip()
        teste = Teste(nome, idade)

        cursor = mysql.connection.cursor()
        query, values = teste.create()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        flash("Teste criado com sucesso!")
    else:
        flash('Inválido!', 'danger')

    return render_template('teste.html')

from flask import Blueprint, render_template, request, flash
from dbContext import mysql
from app.models.aluno import Aluno

bp = Blueprint('aluno', __name__)

@bp.route('/adicionar_aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':
        nome = request.form.get('nome').strip(),
        idade = request.form.get('idade').strip()
        aluno = Aluno(nome, idade)

        cursor = mysql.connection.cursor()
        query, values = aluno.criar_aluno()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        flash("Aluno criado com sucesso!")

        return render_template('index.html')
    else:
        flash('Inválido!', 'danger')

    return render_template('teste.html')
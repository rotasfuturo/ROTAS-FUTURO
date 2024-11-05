import os
from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
from dbContext import mysql, DBContext
from app.models.aluno import Aluno
from app.__init__ import create_app

bp = Blueprint('aluno', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/alunos', methods=['GET'])
def listar_alunos():
    filtro = request.args.get('search')
    cursor = mysql.connection.cursor()
    if filtro:
        pass
    else:
        alunos = Aluno.listar_alunos(cursor)
    data = cursor.fetchall()
    cursor.close()

    return render_template('lista_alunos.html', aluno=data)

@bp.route('/cadastro_aluno', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':
        image = request.files['foto']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(create_app().config['UPLOAD_FOLDER'], filename)
            image.save(filepath)

            nome = request.form.get('nome').strip().upper()
            escola = request.form.get('escola').strip().upper()
            serie = request.form.get('serie').strip().upper()
            turma_escola = request.form.get('turma').strip().upper()
            turno_escola = request.form.get('turno').strip().upper()
            data_cadastro = request.form.get('data_cadastro')
            try:
                data_cadastro_f = datetime.strptime(data_cadastro, '%Y-%m-%d')
            except ValueError:
                return "Data inválida. Por favor, use o formato AAAA-MM-DD."
            data_nasc = request.form.get('data_nasc')
            try:
                data_nasc_f = datetime.strptime(data_nasc, '%Y-%m-%d')
            except ValueError:
                return "Data inválida. Por favor, use o formato AAAA-MM-DD."
            endereco = request.form.get('endereco').strip().upper()
            telefone = request.form.get('telefone').strip()
            filiacao = request.form.get('filiacao').strip().upper()
            responsavel = request.form.get('responsavel').strip().upper()
            beneficio = request.form.get('beneficio').strip().upper()
            acompanhamento = request.form.get('acompanhamento').strip()
            orientacoes = request.form.get('orientacoes').strip()
            image = filename
            aluno = Aluno(nome, escola, serie, turma_escola, turno_escola, data_cadastro, data_nasc, endereco, telefone,
                          filiacao, responsavel, beneficio, acompanhamento, orientacoes, image)

            cursor = mysql.connection.cursor()
            query, values = aluno.criar_aluno()
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            flash("Aluno criado com sucesso!")

            return render_template('index.html')
        else:
            flash('Tipo de arquivo inválido!', 'danger')
    else:
        flash('Inválido!', 'danger')

    return render_template('criar_aluno.html')

@bp.route('/deletar_aluno/<int:_id>', methods=['POST'])
def deletar_aluno(_id):
    cursor = mysql.connection.cursor()
    cursor.execute(f'SELECT FOTO FROM ALUNO WHERE id={_id}')
    aluno = cursor.fetchone()
    cursor.execute(Aluno.deletar_aluno(_id))
    mysql.connection.commit()
    cursor.close()

    if aluno and aluno[0]:
        image_path = os.path.join(create_app().config['UPLOAD_FOLDER'], aluno[0])
        if os.path.exists(image_path):
            os.remove(image_path)
    flash("Data Deleted Successfully!")

    return redirect(url_for('index'))
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
    filtro = request.args.get('pesquisa')
    cursor = mysql.connection.cursor()
    if filtro:
        aluno = Aluno.pesquisar(filtro, cursor)
    else:
        alunos = Aluno.listar_alunos(cursor)
    data = cursor.fetchall()
    cursor.close()

    return render_template('lista_alunos.html', aluno=data)

@bp.route('/aluno/<string:_nome>/<int:_id>', methods=['GET', 'POST'])
def pagina_aluno(_nome, _id):
    cursor = mysql.connection.cursor()
    aluno = Aluno.selecionar_aluno(_id, cursor)
    cursor.close()

    return render_template('pagina_aluno.html', aluno=aluno)


@bp.route('/alunos', methods=['GET', 'POST'])
def adicionar_aluno():
    if request.method == 'POST':

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

        image = request.files['foto'] if 'foto' in request.files else None
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(create_app().config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
            image = filename
        else:
            image = 'none'

        cursor = mysql.connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) FROM ALUNO 
            WHERE NOME = %s AND DATA_NASC = %s AND TELEFONE = %s
        """, (nome, data_nasc_f, telefone))
        aluno_existente = cursor.fetchone()[0]

        if aluno_existente > 0:
            cursor.close()
            flash("Este aluno já está cadastrado!", "danger")
            return redirect(url_for('aluno.adicionar_aluno'))

        aluno = Aluno(nome, escola, serie, turma_escola, turno_escola, data_cadastro, data_nasc, endereco, telefone,
                      filiacao, responsavel, beneficio, acompanhamento, orientacoes, image)

        query, values = aluno.criar_aluno()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()

        flash("Aluno criado com sucesso!", "success")
        return redirect(url_for('aluno.listar_alunos'))
    else:
        flash('Erro ao processar o formulário', 'danger')

    return render_template('lista_alunos.html')


@bp.route('/editar_aluno/<string:_nome>/<int:_id>', methods=['POST', 'GET'])
def atualizar_aluno(_nome, _id):
    aluno = None

    if request.method == 'POST':
        image = request.files.get('foto')
        filename = None

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            filepath = os.path.join(create_app().config['UPLOAD_FOLDER'], filename)
            image.save(filepath)
        else:
            aluno = Aluno.selecionar_aluno(_id, mysql.connection.cursor())
            filename = aluno.foto

        try:
            nome = request.form.get('nome').strip().upper()
            escola = request.form.get('escola').strip().upper()
            serie = request.form.get('serie').strip().upper()
            turma_escola = request.form.get('turma').strip().upper()
            turno_escola = request.form.get('turno').strip().upper()
            data_cadastro = datetime.strptime(request.form.get('data_cadastro'), '%Y-%m-%d')
            data_nasc = datetime.strptime(request.form.get('data_nasc'), '%Y-%m-%d')
            endereco = request.form.get('endereco').strip().upper()
            telefone = request.form.get('telefone').strip()
            filiacao = request.form.get('filiacao').strip().upper()
            responsavel = request.form.get('responsavel').strip().upper()
            beneficio = request.form.get('beneficio').strip().upper()
            acompanhamento = request.form.get('acompanhamento').strip()
            orientacoes = request.form.get('orientacoes').strip()
        except ValueError as e:
            print('erro1')
            flash(f"Erro na entrada de dados: {e}", "danger")
            return redirect(url_for('aluno.pagina_aluno', _id=_id, _nome=_nome))

        aluno = Aluno(nome, escola, serie, turma_escola, turno_escola, data_cadastro, data_nasc, endereco, telefone,
                      filiacao, responsavel, beneficio, acompanhamento, orientacoes, filename)

        try:
            cursor = mysql.connection.cursor()
            query, values = aluno.atualizar_aluno(_id)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            flash("Aluno atualizado com sucesso!", "success")
            return redirect(url_for('aluno.pagina_aluno', _id=_id, _nome=_nome))
        except Exception as e:
            print('erro2')
            flash(f"Erro ao atualizar o aluno: {e}", "danger")
            return redirect(url_for('aluno.pagina_aluno', _id=_id, _nome=_nome))

    else:
        cursor = mysql.connection.cursor()
        aluno = Aluno.selecionar_aluno(_id, cursor)
        cursor.close()

        if not aluno:
            print('erro3')
            flash("Aluno não encontrado.", "danger")
            return redirect(url_for('aluno.listar_alunos'))

    return render_template('pagina_aluno.html', _nome=_nome, _id=_id, aluno=aluno)


@bp.route('/deletar_aluno/<int:_id>', methods=['POST'])
def deletar_aluno(_id):
    cursor = mysql.connection.cursor()

    cursor.execute(f'SELECT FOTO FROM ALUNO WHERE ID_ALUNO = {_id}')
    aluno = cursor.fetchone()

    cursor.execute("""
            SELECT COUNT(*) FROM MATRICULA 
            WHERE ID_ALUNO = %s AND STATUS = 0
        """, (_id,))
    matricula_ativa = cursor.fetchone()[0]

    if matricula_ativa > 0:
        cursor.close()
        flash("Este aluno não pode ser deletado enquanto tiver uma matrícula ativa.", "danger")
        return redirect(url_for('aluno.listar_alunos'))

    cursor.execute(Aluno.deletar_aluno(_id))
    mysql.connection.commit()

    if aluno and aluno[0]:
        image_path = os.path.join(create_app().config['UPLOAD_FOLDER'], aluno[0])
        if os.path.exists(image_path):
            os.remove(image_path)

    cursor.close()
    flash("Aluno deletado com sucesso", "success")

    return redirect(url_for('aluno.listar_alunos'))


@bp.route('/desativar_aluno/<int:_id>', methods=['POST', 'GET'])
def desativar_aluno(_id):
    cursor = mysql.connection.cursor()

    aluno = Aluno.selecionar_aluno(_id, cursor)

    cursor.execute("""
        SELECT COUNT(*) FROM MATRICULA 
        WHERE ID_ALUNO = %s AND STATUS = 0
    """, (_id,))
    matricula_ativa = cursor.fetchone()[0]

    if matricula_ativa > 0:
        cursor.close()
        flash("Este aluno não pode ser desativado enquanto tiver uma matrícula ativa.", "danger")
        return redirect(url_for('aluno.listar_alunos'))

    if aluno.status == 0:
        cursor.execute(Aluno.desativar_aluno(_id))
        mysql.connection.commit()
        cursor.close()
        flash("Aluno desativado com sucesso", "success")
    else:
        cursor.close()
        flash("Aluno já está desativado.", "warning")

    return redirect(url_for('aluno.listar_alunos'))


@bp.route('/ativar_aluno/<int:_id>', methods=['POST', 'GET'])
def ativar_aluno(_id):
    cursor = mysql.connection.cursor()
    aluno = Aluno.selecionar_aluno(_id, cursor)
    if aluno.status == 1:
        cursor.execute(Aluno.ativar_aluno(_id))
        mysql.connection.commit()
        cursor.close()
        flash("Aluno ativado com sucesso", "success")
    else:
        cursor.close()

    return redirect(url_for('aluno.listar_alunos'))
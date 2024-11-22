from flask import Blueprint, render_template, request, flash, redirect, url_for
from dbContext import mysql
from datetime import datetime
from app.models.visita import Visita
from app.models.aluno import Aluno


bp = Blueprint('visita', __name__)

@bp.route('/visitas', methods=['GET'])
def listar_visitas():
    filtro = request.args.get('pesquisa')
    cursor = mysql.connection.cursor()
    if filtro:
        visitas = Visita.pesquisar(filtro, cursor)
    else:
        visitas = Visita.listar_visitas(cursor)

    visitas = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    aluno = Aluno.listar_alunos(cursor)
    alunos = cursor.fetchall()
    cursor.close()

    return render_template('lista_visitas.html', visita=visitas, alunos=alunos)


@bp.route('/visita/<int:_id>', methods=['GET', 'POST'])
def pagina_visita(_id):
    cursor = mysql.connection.cursor()
    visita = Visita.selecionar_visita(_id, cursor)

    Aluno.listar_alunos(cursor)
    alunos = cursor.fetchall()


    query = (f'SELECT ALUNO.NOME, ALUNO.ESCOLA, ALUNO.SERIE, ALUNO.ENDERECO FROM ALUNO '
             f'INNER JOIN VISITA ON ALUNO.ID_ALUNO = VISITA.ID_ALUNO '
             f'WHERE VISITA.ID_VISITA = {_id}')
    cursor.execute(query)
    resultado = cursor.fetchone()

    if resultado:
        nome_aluno, escola_aluno, serie_aluno, endereco_aluno = resultado
    else:
        nome_aluno = escola_aluno = serie_aluno = endereco_aluno = "Informação não encontrada"

    return render_template('pagina_visita.html', visita=visita, alunos=alunos, nome_aluno=nome_aluno,
                           escola_aluno=escola_aluno, serie_aluno=serie_aluno, endereco_aluno=endereco_aluno)

@bp.route('/visitas', methods=['GET', 'POST'])
def adicionar_visita():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ALUNO WHERE STATUS = 0")
    alunos = cursor.fetchall()

    if request.method == 'POST':
        try:
            id_aluno = request.form.get('aluno')
            data = request.form.get('data')
            try:
                data_f = datetime.strptime(data, '%Y-%m-%d')
            except ValueError:
                return "Data inválida. Por favor, use o formato AAAA-MM-DD."
            objetivo = request.form.get('objetivo')
            profissionais = request.form.get('profissionais').upper()
            familia = request.form.get('familia')
            relato = request.form.get('relato')
            conclusao = request.form.get('conclusao')

            cursor = mysql.connection.cursor()

            visita = Visita(id_aluno, data, objetivo,profissionais, familia, relato, conclusao)
            query, values = visita.criar_visita()
            cursor.execute(query, values)

            mysql.connection.commit()
            cursor.close()
            flash("Visita registrada com sucesso!", "success")
            return redirect(url_for('visita.listar_visitas'))

        except Exception as e:
            cursor = mysql.connection.cursor()
            aluno = Aluno.listar_alunos(cursor)
            alunos = cursor.fetchall()
            cursor.close()
            flash(f"Erro ao registrar visita: {e}", "danger")

    return render_template('lista_visitas.html', visita=visita, alunos=alunos)

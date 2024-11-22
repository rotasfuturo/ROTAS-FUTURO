from flask import Blueprint, render_template, request, flash, redirect, url_for
from dbContext import mysql
from datetime import datetime
from app.models.matricula import Matricula
from app.models.atividade import Atividade
from app.models.aluno import Aluno
from app.models.turma import Turma


bp = Blueprint('matricula', __name__)

@bp.route('/matriculas', methods=['GET'])
def listar_matriculas():
    filtro = request.args.get('pesquisa')
    cursor = mysql.connection.cursor()
    if filtro:
        matricula = Matricula.pesquisar(filtro, cursor)
    else:
        matriculas = Matricula.listar_matriculas(cursor)
    data = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    aluno = Aluno.listar_alunos(cursor)
    alunos = cursor.fetchall()
    atividade = Atividade.listar_atividades(cursor)
    atividades = cursor.fetchall()
    turma = Turma.listar_turmas(cursor)
    turmas = cursor.fetchall()
    cursor.close()

    return render_template('lista_matriculas.html', matricula=data, alunos=alunos, turmas=turmas, atividades=atividades)

@bp.route('/matricula/<int:_id>', methods=['GET', 'POST'])
def pagina_matricula(_id):
    cursor = mysql.connection.cursor()
    matricula = Matricula.selecionar_matricula(_id, cursor)

    Atividade.listar_atividades(cursor)
    atividades = cursor.fetchall()

    Aluno.listar_alunos(cursor)
    alunos = cursor.fetchall()

    Turma.listar_turmas(cursor)
    turmas = cursor.fetchall()

    query = (f'SELECT ALUNO.NOME FROM ALUNO '
             f'INNER JOIN MATRICULA ON ALUNO.ID_ALUNO = MATRICULA.ID_ALUNO '
             f'WHERE MATRICULA.ID_MATRICULA = {_id}')
    cursor.execute(query)
    nome_aluno = cursor.fetchone()
    query = (f'SELECT ATIVIDADE.NOME FROM ATIVIDADE '
             f'INNER JOIN MATRICULA ON ATIVIDADE.ID_ATIVIDADE = MATRICULA.ID_ATIVIDADE '
             f'WHERE MATRICULA.ID_MATRICULA = {_id}')
    cursor.execute(query)
    nome_atividade = cursor.fetchone()
    query = (f'SELECT TURMA.NOME FROM TURMA '
             f'INNER JOIN MATRICULA ON TURMA.ID_TURMA = MATRICULA.ID_TURMA '
             f'WHERE MATRICULA.ID_MATRICULA = {_id}')
    cursor.execute(query)
    nome_turma = cursor.fetchone()
    cursor.close()

    return render_template('pagina_matricula.html', matricula=matricula, alunos=alunos, atividades=atividades,
                           turmas=turmas, nome_aluno=nome_aluno, nome_atividade=nome_atividade, nome_turma=nome_turma)

@bp.route('/matriculas', methods=['GET', 'POST'])
def adicionar_matricula():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM ALUNO WHERE STATUS = 0")
    alunos = cursor.fetchall()
    cursor.execute("SELECT * FROM ATIVIDADE WHERE STATUS = 0")
    atividades = cursor.fetchall()
    cursor.execute("SELECT * FROM TURMA WHERE STATUS = 0")
    turmas = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        try:
            id_aluno = request.form.get('aluno')
            id_atividade = request.form.get('atividade')
            id_turma = request.form.get('turma')
            data = request.form.get('data_matricula')
            try:
                data_f = datetime.strptime(data, '%Y-%m-%d')
            except ValueError:
                return "Data inválida. Por favor, use o formato AAAA-MM-DD."

            cursor = mysql.connection.cursor()
            cursor.execute("SELECT QUANTIDADE_ALUNOS, QUANTIDADE_MAX_ALUNOS FROM TURMA WHERE ID_TURMA = %s",
                           id_turma)
            turma = cursor.fetchone()
            if not turma:
                flash("Turma não encontrada.", "danger")
                cursor.close()
                return redirect(url_for('matricula.adicionar_matricula'))

            quantidade_alunos, quantidade_max_alunos = turma
            if quantidade_alunos >= quantidade_max_alunos:
                flash("A turma já atingiu o número máximo de vagas.", "danger")
                cursor.close()
                return redirect(url_for('matricula.adicionar_matricula'))

            cursor.execute("SELECT * FROM MATRICULA WHERE ID_ALUNO = %s AND ID_ATIVIDADE = %s",
                           (id_aluno, id_atividade))
            matricula_existente = cursor.fetchone()

            if matricula_existente:
                flash("O aluno já está matriculado nesta atividade.", "danger")
                cursor.close()
                return redirect(url_for('matricula.adicionar_matricula'))

            matricula = Matricula(id_atividade, id_aluno, id_turma, data)
            query, values = matricula.criar_matricula()
            cursor.execute(query, values)

            Turma.adicionar_aluno_turma(id_turma, cursor)

            mysql.connection.commit()
            cursor.close()
            flash("Aluno matriculado com sucesso!", "success")
            return redirect(url_for('matricula.listar_matriculas'))

        except Exception as e:
            cursor = mysql.connection.cursor()
            aluno = Aluno.listar_alunos(cursor)
            alunos = cursor.fetchall()
            atividade = Atividade.listar_atividades(cursor)
            atividades = cursor.fetchall()
            turma = Turma.listar_turmas(cursor)
            turmas = cursor.fetchall()
            cursor.close()
            flash(f"Erro ao matricular aluno: {e}", "danger")

    return render_template('lista_matriculas.html', matricula=matricula, alunos=alunos, atividades=atividades, turmas=turmas)


@bp.route('/deletar_matricula/<int:_id>', methods=['POST'])
def deletar_matricula(_id):
    cursor = mysql.connection.cursor()
    cursor.execute(Matricula.deletar_matricula(_id))
    query = (f'SELECT TURMA.ID_TURMA FROM TURMA '
             f'INNER JOIN MATRICULA ON TURMA.ID_TURMA = MATRICULA.ID_TURMA '
             f'WHERE MATRICULA.ID_MATRICULA = {_id}')
    cursor.execute(query)
    id_turma = cursor.fetchone()

    if not id_turma:
        flash("Erro: Matrícula não encontrada ou já foi deletada.", "danger")
        return redirect(url_for('matricula.listar_matriculas'))

    Turma.deletar_aluno_turma(id_turma, cursor)
    mysql.connection.commit()
    cursor.close()
    flash("Matrícula deletada com sucesso", "success")

    return redirect(url_for('matricula.listar_matriculas'))

@bp.route('/desativar_matricula/<int:_id>', methods=['POST', 'GET'])
def desativar_matricula(_id):
    cursor = mysql.connection.cursor()
    matricula = Matricula.selecionar_matricula(_id, cursor)
    if matricula.status == 0:
        cursor.execute(Matricula.desativar_matricula(_id))
        query = (f'SELECT TURMA.ID_TURMA FROM TURMA '
                 f'INNER JOIN MATRICULA ON TURMA.ID_TURMA = MATRICULA.ID_TURMA '
                 f'WHERE MATRICULA.ID_MATRICULA = {_id}')
        cursor.execute(query)
        id_turma = cursor.fetchone()

        if not id_turma:
            flash("Erro: Matrícula não encontrada ou já foi deletada.", "danger")
            return redirect(url_for('matricula.listar_matriculas'))

        Turma.deletar_aluno_turma(id_turma, cursor)
        mysql.connection.commit()
        cursor.close()
        flash("Matrícula desativada com sucesso", "success")
    else:
        cursor.close()

    return redirect(url_for('matricula.listar_matriculas'))

@bp.route('/ativar_matricula/<int:_id>', methods=['POST', 'GET'])
def ativar_matricula(_id):
    cursor = mysql.connection.cursor()
    matricula = Matricula.selecionar_matricula(_id, cursor)
    if matricula.status == 1:
        cursor.execute(Matricula.ativar_matricula(_id))
        query = (f'SELECT TURMA.ID_TURMA FROM TURMA '
                 f'INNER JOIN MATRICULA ON TURMA.ID_TURMA = MATRICULA.ID_TURMA '
                 f'WHERE MATRICULA.ID_MATRICULA = {_id}')
        cursor.execute(query)
        id_turma = cursor.fetchone()
        Turma.adicionar_aluno_turma(id_turma, cursor)
        mysql.connection.commit()
        cursor.close()
        flash("Matrícula ativada com sucesso", "success")
    else:
        cursor.close()

    return redirect(url_for('matricula.listar_matriculas'))
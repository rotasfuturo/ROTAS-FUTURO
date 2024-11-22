from flask import Blueprint, render_template, request, flash, redirect, url_for
from dbContext import mysql
from app.models.atividade import Atividade
from app.models.professor import Professor

bp = Blueprint('atividade', __name__)

@bp.route('/atividades', methods=['GET'])
def listar_atividades():
    filtro = request.args.get('pesquisa')
    cursor = mysql.connection.cursor()
    if filtro:
        atividade = Atividade.pesquisar(filtro, cursor)
    else:
        atividades = Atividade.listar_atividades(cursor)
    data = cursor.fetchall()
    cursor.close()

    cursor = mysql.connection.cursor()
    professor = Professor.listar_professores(cursor)
    professores = cursor.fetchall()
    cursor.close()

    return render_template('lista_atividades.html', atividade=data, professores=professores)

@bp.route('/atividade/<int:_id>', methods=['GET', 'POST'])
def pagina_atividade(_id):
    cursor = mysql.connection.cursor()
    atividade = Atividade.selecionar_atividade(_id, cursor)
    professor = Professor.listar_professores(cursor)
    professores = cursor.fetchall()
    query = (f'SELECT PROFESSOR.NOME FROM PROFESSOR '
             f'INNER JOIN ATIVIDADE ON PROFESSOR.ID_PROFESSOR = ATIVIDADE.ID_PROFESSOR '
             f'WHERE ATIVIDADE.ID_ATIVIDADE = {_id}')
    cursor.execute(query)
    nome_professor = cursor.fetchone()
    cursor.close()

    return render_template('pagina_atividade.html', atividade=atividade, professores=professores,
                           nome_professor=nome_professor)


@bp.route('/atividades', methods=['GET', 'POST'])
def adicionar_atividade():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM PROFESSOR WHERE STATUS = 0")
    professores = cursor.fetchall()
    cursor.close()

    if request.method == 'POST':
        try:
            id_professor = request.form.get('professor')
            nome = request.form.get('nome').strip().upper()
            atividade = Atividade(id_professor, nome)

            cursor = mysql.connection.cursor()
            query, values = atividade.criar_atividade()
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()

            flash("Atividade criada com sucesso!", "success")
            return redirect(url_for('atividade.listar_atividades'))
        except Exception as e:
            cursor = mysql.connection.cursor()
            professor = Professor.listar_professores(cursor)
            professores = cursor.fetchall()
            cursor.close()
            flash(f"Erro ao criar atividade: {e}", "danger")

    return render_template('lista_atividades.html', professores=professores)


@bp.route('/editar_atividade/<int:_id>', methods=['POST', 'GET'])
def atualizar_atividade(_id):
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM PROFESSOR WHERE STATUS = 0")
    professores = cursor.fetchall()
    cursor.close()

    atividade = None
    if request.method == 'POST':
        try:
            id_professor = int(request.form.get('professor'))
            nome = request.form.get('nome').strip().upper()

        except ValueError as e:
            flash(f"Erro na entrada de dados: {e}", "danger")
            return redirect(url_for('atividade.pagina_atividade', _id=_id))

        atividade = Atividade(id_professor, nome)

        try:
            cursor = mysql.connection.cursor()
            query, values = atividade.atualizar_atividade(_id)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            flash("Atividade atualizada com sucesso!", "success")
            return redirect(url_for('atividade.pagina_atividade', _id=_id))

        except Exception as e:
            flash(f"Erro ao atualizar a atividade: {e}", "danger")
            return redirect(url_for('atividade.pagina_atividade', _id=_id))

    else:
        cursor = mysql.connection.cursor()
        atividade = Atividade.selecionar_atividade(_id, cursor)
        cursor.close()

        if not atividade:
            flash("Atividade não encontrada.", "danger")
            return redirect(url_for('home.home'))

    return render_template('pagina_atividade.html', atividade=atividade, professores=professores)


@bp.route('/deletar_atividade/<int:_id>', methods=['POST'])
def deletar_atividade(_id):
    cursor = mysql.connection.cursor()

    cursor.execute("""
                SELECT COUNT(*) FROM MATRICULA 
                WHERE ID_ATIVIDADE = %s AND STATUS = 0
            """, (_id,))
    matricula_ativa = cursor.fetchone()[0]

    if matricula_ativa > 0:
        cursor.close()
        flash("Esta atividade não pode ser deletada enquanto tiver uma matrícula ativa.", "danger")
        return redirect(url_for('atividade.listar_atividades'))

    cursor.execute(Atividade.deletar_atividade(_id))
    mysql.connection.commit()
    cursor.close()
    flash("Atividade deletada com sucesso", "success")

    return redirect(url_for('atividade.listar_atividades'))

@bp.route('/desativar_atividade/<int:_id>', methods=['POST', 'GET'])
def desativar_atividade(_id):
    cursor = mysql.connection.cursor()
    atividade = Atividade.selecionar_atividade(_id, cursor)

    cursor.execute("""
            SELECT COUNT(*) FROM MATRICULA 
            WHERE ID_ATIVIDADE = %s AND STATUS = 0
        """, (_id,))
    matricula_ativa = cursor.fetchone()[0]

    if matricula_ativa > 0:
        cursor.close()
        flash("Esta atividade não pode ser desativada enquanto tiver uma matrícula ativa.", "danger")
        return redirect(url_for('atividade.listar_atividades'))

    if atividade.status == 0:
        cursor.execute(Atividade.desativar_atividade(_id))
        mysql.connection.commit()
        cursor.close()
        flash("Atividade desativada com sucesso", "success")
    else:
        cursor.close()

    return redirect(url_for('atividade.listar_atividades'))

@bp.route('/ativar_atividade/<int:_id>', methods=['POST', 'GET'])
def ativar_atividade(_id):
    cursor = mysql.connection.cursor()
    atividade = Atividade.selecionar_atividade(_id, cursor)
    if atividade.status == 1:
        cursor.execute(Atividade.ativar_atividade(_id))
        mysql.connection.commit()
        cursor.close()
        flash("Atividade ativada com sucesso", "success")
    else:
        cursor.close()

    return redirect(url_for('atividade.listar_atividades'))
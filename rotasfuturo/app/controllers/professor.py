from flask import Blueprint, render_template, request, flash, redirect, url_for
from dbContext import mysql
from app.models.professor import Professor

bp = Blueprint('professor', __name__)

@bp.route('/professores', methods=['GET'])
def listar_professores():
    filtro = request.args.get('pesquisa')
    cursor = mysql.connection.cursor()
    if filtro:
        professor = Professor.pesquisar(filtro, cursor)
    else:
        professores = Professor.listar_professores(cursor)
    data = cursor.fetchall()
    cursor.close()

    return render_template('lista_professores.html', professor=data)

@bp.route('/professor/<string:_nome>/<int:_id>', methods=['GET', 'POST'])
def pagina_professor(_nome, _id):
    cursor = mysql.connection.cursor()
    professor = Professor.selecionar_professor(_id, cursor)
    return render_template('pagina_professor.html', professor=professor)

@bp.route('/professores', methods=['GET', 'POST'])
def adicionar_professor():
    if request.method == 'POST':
        nome = request.form.get('nome').strip().upper()
        telefone = request.form.get('telefone').strip()
        professor = Professor(nome, telefone)
        cursor = mysql.connection.cursor()
        query, values = professor.criar_professor()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        flash("Professor criado com sucesso!", "success")

        return redirect(url_for('professor.listar_professores'))
    else:
        flash('Inválido!', 'danger')

    return render_template('lista_professores.html')

@bp.route('/editar_professor/<string:_nome>/<int:_id>', methods=['POST', 'GET'])
def atualizar_professor(_nome, _id):
    professor = None

    if request.method == 'POST':
        try:
            nome = request.form.get('nome').strip().upper()
            telefone = request.form.get('telefone').strip()

        except ValueError as e:
            flash(f"Erro na entrada de dados: {e}", "danger")
            return redirect(url_for('professor.pagina_professor', _nome=_nome, _id=_id))

        professor = Professor(nome, telefone)

        try:
            cursor = mysql.connection.cursor()
            query, values = professor.atualizar_professor(_id)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            flash("Professor atualizado com sucesso!", "success")
            return redirect(url_for('professor.pagina_professor', _nome=_nome, _id=_id))

        except Exception as e:
            flash(f"Erro ao atualizar o professor: {e}", "danger")
            return redirect(url_for('professor.pagina_professor', _nome=_nome, _id=_id))

    else:
        cursor = mysql.connection.cursor()
        professor = Professor.selecionar_professor(_id, cursor)
        cursor.close()

        if not professor:
            flash("Professor não encontrado.", "danger")
            return redirect(url_for('home.home'))

    return render_template('pagina_professor.html', _nome=_nome, _id=_id, professor=professor)


@bp.route('/deletar_professor/<int:_id>', methods=['POST'])
def deletar_professor(_id):
    cursor = mysql.connection.cursor()

    cursor.execute("""
                SELECT COUNT(*) FROM ATIVIDADE
                WHERE ID_PROFESSOR = %s AND STATUS = 0
            """, (_id,))
    atividade_ativa = cursor.fetchone()[0]

    if atividade_ativa > 0:
        cursor.close()
        flash("Este professor não pode ser deletado enquanto tiver uma atividade ativa.", "danger")
        return redirect(url_for('professor.listar_professores'))

    cursor.execute(Professor.deletar_professor(_id))
    mysql.connection.commit()
    cursor.close()
    flash("Professor deletado com sucesso", "success")

    return redirect(url_for('professor.listar_professores'))

@bp.route('/desativar_professor/<int:_id>', methods=['POST', 'GET'])
def desativar_professor(_id):
    cursor = mysql.connection.cursor()
    professor = Professor.selecionar_professor(_id, cursor)
    cursor.execute("""
                    SELECT COUNT(*) FROM ATIVIDADE
                    WHERE ID_PROFESSOR = %s AND STATUS = 0
                """, (_id,))
    atividade_ativa = cursor.fetchone()[0]

    if atividade_ativa > 0:
        cursor.close()
        flash("Este professor não pode ser desativado enquanto tiver uma atividade ativa.", "danger")
        return redirect(url_for('professor.listar_professores'))

    if professor.status == 0:
        cursor.execute(Professor.desativar_professor(_id))
        mysql.connection.commit()
        cursor.close()
        flash("Professor desativado com sucesso", "success")
    else:
        cursor.close()

    return redirect(url_for('professor.listar_professores'))

@bp.route('/ativar_professor/<int:_id>', methods=['POST', 'GET'])
def ativar_professor(_id):
    cursor = mysql.connection.cursor()
    professor = Professor.selecionar_professor(_id, cursor)
    if professor.status == 1:
        cursor.execute(Professor.ativar_professor(_id))
        mysql.connection.commit()
        cursor.close()
        flash("Professor ativado com sucesso", "success")
    else:
        cursor.close()

    return redirect(url_for('professor.listar_professores'))
from flask import Blueprint, render_template, request, flash, redirect, url_for
from dbContext import mysql
from app.models.turma import Turma

bp = Blueprint('turma', __name__)

@bp.route('/turmas', methods=['GET'])
def listar_turmas():
    filtro = request.args.get('pesquisa')
    cursor = mysql.connection.cursor()
    if filtro:
        turma = Turma.pesquisar(filtro, cursor)
    else:
        turmas = Turma.listar_turmas(cursor)
    data = cursor.fetchall()
    cursor.close()

    return render_template('lista_turmas.html', turma=data)

@bp.route('/turma/<int:_id>', methods=['GET', 'POST'])
def pagina_turma(_id):
    cursor = mysql.connection.cursor()
    turma = Turma.selecionar_turma(_id, cursor)
    return render_template('pagina_turma.html', turma=turma)

@bp.route('/turmas', methods=['GET', 'POST'])
def adicionar_turma():
    if request.method == 'POST':
        periodo = request.form.get('periodo').strip().upper()
        nome = request.form.get('nome').strip().upper()
        qtd_max_alunos = request.form.get('qtd_max_alunos').strip()
        turma = Turma(periodo, nome, qtd_max_alunos)
        cursor = mysql.connection.cursor()
        query, values = turma.criar_turma()
        cursor.execute(query, values)
        mysql.connection.commit()
        cursor.close()
        flash("Turma criada com sucesso!", "success")

        return redirect(url_for('turma.listar_turmas'))
    else:
        flash('Inválido!', 'danger')

    return render_template('lista_turmas.html')

@bp.route('/editar_turma/<int:_id>', methods=['POST', 'GET'])
def atualizar_turma(_id):
    turma = None

    if request.method == 'POST':
        try:
            periodo = request.form.get('periodo').strip().upper()
            nome = request.form.get('nome').strip().upper()
            qtd_max_alunos = request.form.get('qtd_max_alunos').strip().upper()

        except ValueError as e:
            flash(f"Erro na entrada de dados: {e}", "danger")
            return redirect(url_for('turma.listar_turmas'))

        turma = Turma(periodo, nome, qtd_max_alunos)

        try:
            cursor = mysql.connection.cursor()
            query, values = turma.atualizar_turma(_id)
            cursor.execute(query, values)
            mysql.connection.commit()
            cursor.close()
            flash("Turma atualizada com sucesso!", "success")
            return redirect(url_for('turma.listar_turmas'))
        except Exception as e:
            flash(f"Erro ao atualizar a turma: {e}", "danger")
            return redirect(url_for('turma.listar_turmas'))

    else:
        cursor = mysql.connection.cursor()
        turma = Turma.selecionar_turma(_id, cursor)
        cursor.close()

        if not turma:
            flash("Turma não encontrada.", "danger")
            return redirect(url_for('home.home'))

    return render_template('lista_turmas.html', _id=_id, turma=turma)

@bp.route('/deletar_turma/<int:_id>', methods=['POST'])
def deletar_turma(_id):
    cursor = mysql.connection.cursor()

    cursor.execute("""
                    SELECT COUNT(*) FROM MATRICULA
                    WHERE ID_TURMA = %s AND STATUS = 0
                """, (_id,))
    matricula_ativa = cursor.fetchone()[0]

    if matricula_ativa > 0:
        cursor.close()
        flash("Esta turma não pode ser deletada enquanto tiver uma matrícula ativa.", "danger")
        return redirect(url_for('turma.listar_turmas'))

    cursor.execute(Turma.deletar_turma(_id))
    mysql.connection.commit()
    cursor.close()
    flash("Turma deletada com sucesso", "success")

    return redirect(url_for('turma.listar_turmas'))

@bp.route('/desativar_turma/<int:_id>', methods=['POST', 'GET'])
def desativar_turma(_id):
    cursor = mysql.connection.cursor()
    turma = Turma.selecionar_turma(_id, cursor)

    cursor.execute("""
                        SELECT COUNT(*) FROM MATRICULA
                        WHERE ID_TURMA = %s AND STATUS = 0
                    """, (_id,))
    matricula_ativa = cursor.fetchone()[0]

    if matricula_ativa > 0:
        cursor.close()
        flash("Esta turma não pode ser deletada enquanto tiver uma matrícula ativa.", "danger")
        return redirect(url_for('turma.listar_turmas'))

    if turma.status == 0:
        cursor.execute(Turma.desativar_turma(_id))
        mysql.connection.commit()
        cursor.close()
        flash("Turma desativada com sucesso", "success")
    else:
        cursor.close()

    return redirect(url_for('turma.listar_turmas'))

@bp.route('/ativar_turma/<int:_id>', methods=['POST', 'GET'])
def ativar_turma(_id):
    cursor = mysql.connection.cursor()
    atividade = Turma.selecionar_turma(_id, cursor)
    if atividade.status == 1:
        cursor.execute(Turma.ativar_turma(_id))
        mysql.connection.commit()
        cursor.close()
        flash("Turma ativada com sucesso", "success")
    else:
        cursor.close()

    return redirect(url_for('turma.listar_turmas'))

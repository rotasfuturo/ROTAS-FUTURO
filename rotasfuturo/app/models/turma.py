class Turma:
    def __init__(self, periodo, nome, quantidade_max_alunos):
        self.periodo : str = periodo
        self.nome : str = nome
        self.status : int = 0
        self.quantidade_alunos : int = 0
        self.quantidade_max_alunos : int = quantidade_max_alunos

    @classmethod
    def adicionar_aluno_turma(self, id, cursor):
        query = f'UPDATE TURMA SET QUANTIDADE_ALUNOS = QUANTIDADE_ALUNOS + 1 WHERE ID_TURMA = {id}'

        cursor.execute(query)

    @classmethod
    def deletar_aluno_turma(self, id, cursor):
        query = f'UPDATE TURMA SET QUANTIDADE_ALUNOS = QUANTIDADE_ALUNOS - 1 WHERE ID_TURMA = {id}'

        cursor.execute(query)

    @classmethod
    def listar_turmas(cls, cursor):
        cursor.execute('SELECT * FROM TURMA')

    @classmethod
    def selecionar_turma(cls, id: int, cursor):
        query = '''
                        SELECT ID_TURMA, PERIODO, NOME, STATUS, QUANTIDADE_ALUNOS, QUANTIDADE_MAX_ALUNOS
                        FROM TURMA WHERE ID_TURMA = %s
                    '''
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            turma = Turma(result[1], result[2], result[5])
            turma.id = result[0]
            turma.status = result[3]
            turma.quantidade_alunos = result[4]
            return turma
        else:
            return None

    def criar_turma(self):
        query = 'INSERT INTO TURMA (PERIODO, NOME, STATUS, QUANTIDADE_ALUNOS, QUANTIDADE_MAX_ALUNOS) VALUES (%s, %s, %s, %s, %s)'
        values = (self.periodo, self.nome, self.status, self.quantidade_alunos, self.quantidade_max_alunos)

        return query, values

    def atualizar_turma(self, id: int):
        query = (f'UPDATE TURMA SET PERIODO = %s, NOME = %s, QUANTIDADE_MAX_ALUNOS = %s WHERE ID_TURMA = {id}')
        values = (self.periodo, self.nome, self.quantidade_max_alunos)

        return query, values

    @classmethod
    def deletar_turma(cls, id: int):
        query = (f'DELETE FROM TURMA WHERE ID_TURMA = {id}')

        return query

    @classmethod
    def desativar_turma(cls, id: int):
        query = (f'UPDATE TURMA SET STATUS = 1 WHERE ID_TURMA = {id}')

        return query

    @classmethod
    def ativar_turma(cls, id: int):
        query = (f'UPDATE TURMA SET STATUS = 0 WHERE ID_TURMA = {id}')

        return query

    @classmethod
    def pesquisar(cls, pesquisa, cursor):
        query = "SELECT * FROM TURMA WHERE NOME LIKE %s OR ID_TURMA LIKE %s OR PERIODO LIKE %s"
        cursor.execute(query, (f'%{pesquisa}%', f'%{pesquisa}%', f'%{pesquisa}%'))

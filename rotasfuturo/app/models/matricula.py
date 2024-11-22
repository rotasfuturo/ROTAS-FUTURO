class Matricula:
    def __init__(self, id_atividade, id_aluno, id_turma, data):
        self.id_atividade: int = id_atividade
        self.id_aluno: int = id_aluno
        self.id_turma: int = id_turma
        self.data: str = data
        self.status: int = 0

    @classmethod
    def listar_matriculas(cls, cursor):
        query = """
            SELECT 
            MATRICULA.ID_MATRICULA AS MATRICULA_ID,
            ALUNO.NOME AS ALUNO_NOME,
            ATIVIDADE.NOME AS ATIVIDADE_NOME,
            TURMA.NOME AS TURMA_NOME,
            MATRICULA.DATA
            FROM 
                MATRICULA
            JOIN 
                ALUNO ON MATRICULA.ID_ALUNO = ALUNO.ID_ALUNO
            JOIN 
                ATIVIDADE ON MATRICULA.ID_ATIVIDADE = ATIVIDADE.ID_ATIVIDADE
            JOIN 
                TURMA ON MATRICULA.ID_TURMA = TURMA.ID_TURMA
            ORDER BY MATRICULA.ID_MATRICULA;
            """
        cursor.execute(query)

    @classmethod
    def selecionar_matricula(cls, id: int, cursor):
        cursor.execute(f'SELECT ID_MATRICULA, ID_ATIVIDADE, ID_ALUNO, ID_TURMA, DATA, STATUS FROM MATRICULA WHERE ID_MATRICULA={id}')
        result = cursor.fetchone()
        if result:
            matricula = Matricula(result[1], result[2], result[3], result[4])
            matricula.id = result[0]
            matricula.status = result[5]
            return matricula
        else:
            return None

    def criar_matricula(self):
        query = 'INSERT INTO MATRICULA (ID_ATIVIDADE, ID_ALUNO, ID_TURMA, DATA, STATUS) VALUES (%s, %s, %s, %s, %s)'
        values = (self.id_atividade, self.id_aluno, self.id_turma, self.data, self.status)

        return query, values

    @classmethod
    def deletar_matricula(cls, id: int):
        query = (f'DELETE FROM MATRICULA WHERE ID_MATRICULA = {id}')

        return query

    @classmethod
    def desativar_matricula(cls, id: int):
        query = (f'UPDATE MATRICULA SET STATUS = 1 WHERE ID_MATRICULA = {id}')

        return query

    @classmethod
    def ativar_matricula(cls, id: int):
        query = (f'UPDATE MATRICULA SET STATUS = 0 WHERE ID_MATRICULA = {id}')

        return query

    @classmethod
    def pesquisar(cls, pesquisa, cursor):
        query = """
        SELECT 
            MATRICULA.ID_MATRICULA AS MATRICULA_ID,
            ALUNO.NOME AS ALUNO_NOME,
            ATIVIDADE.NOME AS ATIVIDADE_NOME,
            TURMA.NOME AS TURMA_NOME,
            MATRICULA.DATA
        FROM 
            MATRICULA
        JOIN 
            ALUNO ON MATRICULA.ID_ALUNO = ALUNO.ID_ALUNO
        JOIN 
            ATIVIDADE ON MATRICULA.ID_ATIVIDADE = ATIVIDADE.ID_ATIVIDADE
        JOIN 
            TURMA ON MATRICULA.ID_TURMA = TURMA.ID_TURMA
        WHERE 
            ALUNO.NOME LIKE %s OR ATIVIDADE.NOME LIKE %s OR TURMA.NOME LIKE %s OR MATRICULA.ID_MATRICULA LIKE %s;
        """
        cursor.execute(query, (f"%{pesquisa}%", f"%{pesquisa}%", f"%{pesquisa}%", f"%{pesquisa}%"))

class Professor:
    def __init__(self, nome, telefone):
        self.nome: str = nome
        self.telefone: int = telefone
        self.status: int = 0  # 0 siginifica que o registro está ativo

    @classmethod
    def listar_professores(cls, cursor):
        cursor.execute('SELECT * FROM PROFESSOR')

    @classmethod
    def selecionar_professor(cls, id: int, cursor):
        cursor.execute(f'SELECT ID_PROFESSOR, NOME, TELEFONE, STATUS FROM PROFESSOR WHERE ID_PROFESSOR={id}')
        result = cursor.fetchone()
        if result:
            professor = Professor(result[1], result[2])
            professor.id = result[0]
            professor.status = result[3]
            return professor
        else:
            return None

    def criar_professor(self):
        query = ('INSERT INTO PROFESSOR (NOME, TELEFONE, STATUS) VALUES (%s, %s, %s)')
        values = (self.nome, self.telefone, self.status)

        return query, values

    def atualizar_professor(self, id: int):
        query = '''UPDATE PROFESSOR SET NOME = %s, TELEFONE = %s WHERE ID_PROFESSOR = %s'''
        values = (self.nome, self.telefone, id)

        return query, values

    @classmethod
    def deletar_professor(cls, id: int):
        query = (f'DELETE FROM PROFESSOR WHERE ID_PROFESSOR = {id}')

        return query

    @classmethod
    def desativar_professor(cls, id: int):
        query = (f'UPDATE PROFESSOR SET STATUS = 1 WHERE ID_PROFESSOR = {id}')

        return query

    @classmethod
    def ativar_professor(cls, id: int):
        query = (f'UPDATE PROFESSOR SET STATUS = 0 WHERE ID_PROFESSOR = {id}')

        return query

    @classmethod
    def pesquisar(cls, pesquisa, cursor):
        query = "SELECT * FROM PROFESSOR WHERE NOME LIKE %s OR ID_PROFESSOR LIKE %s"
        cursor.execute(query, (f'%{pesquisa}%', f'%{pesquisa}%'))
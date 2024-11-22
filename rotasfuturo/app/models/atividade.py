class Atividade:
    def __init__(self, id_professor, nome):
        self.id_professor : int = id_professor
        self.nome : str = nome
        self.status : int = 0

    @classmethod
    def listar_atividades(cls, cursor):
        cursor.execute('SELECT * FROM ATIVIDADE')

    @classmethod
    def selecionar_atividade(cls, id: int, cursor):
        query = '''
                    SELECT ID_ATIVIDADE, ID_PROFESSOR, NOME, STATUS
                    FROM ATIVIDADE WHERE ID_ATIVIDADE = %s
                '''
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            atividade = Atividade(result[1], result[2])
            atividade.id = result[0]
            atividade.status = result[3]
            return atividade
        else:
            return None

    def criar_atividade(self):
        query = 'INSERT INTO ATIVIDADE (ID_PROFESSOR, NOME, STATUS) VALUES (%s, %s, %s)'
        values = (self.id_professor, self.nome, self.status)

        return query, values

    def atualizar_atividade(self, id: int):
        query = '''
            UPDATE ATIVIDADE
            SET ID_PROFESSOR = %s, NOME = %s
            WHERE ID_ATIVIDADE = %s
        '''
        values = (self.id_professor, self.nome, id)

        return query, values

    @classmethod
    def deletar_atividade(cls, id: int):
        query = (f'DELETE FROM ATIVIDADE WHERE ID_ATIVIDADE = {id}')

        return query

    @classmethod
    def desativar_atividade(cls, id: int):
        query = (f'UPDATE ATIVIDADE SET STATUS = 1 WHERE ID_ATIVIDADE = {id}')

        return query

    @classmethod
    def ativar_atividade(cls, id: int):
        query = (f'UPDATE ATIVIDADE SET STATUS = 0 WHERE ID_ATIVIDADE = {id}')

        return query

    @classmethod
    def pesquisar(cls, pesquisa, cursor):
        query = "SELECT * FROM ATIVIDADE WHERE NOME LIKE %s OR ID_ATIVIDADE LIKE %s"
        cursor.execute(query, (f'%{pesquisa}%', f'%{pesquisa}%'))

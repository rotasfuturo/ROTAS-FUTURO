class Atividade:
    def __init__(self, id_professor, nome):
        self.id_professor : int = id_professor
        self.nome : str = nome
        self.status : int = 0

    def criar_atividade(self):
        query = 'INSERT INTO ATIVIDADE (ID_PROFESSOR, NOME) VALUES (%s, %s)'
        values = (self.id_professor, self.nome)

        return query, values

class Turma:
    def __init__(self, periodo, nome):
        self.periodo : str = periodo
        self.nome : str = nome
        self.status : int = 0

    def criar_turma(self):
        query = 'INSERT INTO TURMA (PERIODO, NOME) VALUES (%s, %s)'
        values = (self.periodo, self.nome)

        return query, values

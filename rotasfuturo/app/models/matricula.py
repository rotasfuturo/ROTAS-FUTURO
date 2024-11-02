class Matricula:
    def __init__(self, id_atividade, id_aluno, id_turma, data):
        self.id_atividade: int = id_atividade
        self.id_aluno: int = id_aluno
        self.id_turma: int = id_turma
        self.frequencia: int = 0
        self.data: str = data
        self.status: int = 0

    def criar_matricula(self):
        query = 'INSERT INTO MATRICULA (ID_ATIVIDADE, ID_ALUNO, ID_TURMA, DATA) VALUES (%s, %s, %s, %s)'
        values = (self.id_atividade, self.id_aluno, self.id_turma, self.data)

        return query, values

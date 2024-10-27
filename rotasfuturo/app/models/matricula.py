class Matricula:
    def __init__(self, id_atividade, id_aluno, id_turma, 
    frequencia, data, status):
        self.id_atividade : int = id_atividade
        self.id_aluno : int = id_aluno
        self.id_turma : int = id_turma
        self.frequencia : int = frequencia
        self.data : str = data
        self.status : int = status

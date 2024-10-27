from datetime import datetime

class Aluno:
    def __init__(self, nome, escola, serie, turma_escola, 
    turno_escola, data_cadastro, data_nasci, endereco, telefone, 
    filiacao, responsavel, beneficio, acompanhamento, orientacoes,
    foto, status):
        self.nome : str = nome
        self.escola : str = escola
        self.serie : str = serie
        self.turma_escola : str = turma_escola
        self.turno_escola : str = turno_escola
        self.data_cadastro : str = data_cadastro
        self.data_nasci : str = data_nasci
        self.endereco : str = endereco
        self.telefone : int = telefone
        self.filiacao : str = filiacao
        self.responsavel : str = responsavel
        self.beneficio : str = beneficio
        self.acompanhamento : str = acompanhamento
        self.orientacoes : str = orientacoes
        self.foto : str = foto
        self.status : int = status

    


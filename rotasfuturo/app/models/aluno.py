class Aluno:
    def __init__(self, nome, escola, serie, turma_escola,
                 turno_escola, data_cadastro, data_nasc, endereco, telefone,
                 filiacao, responsavel, beneficio, acompanhamento, orientacoes,
                 foto):
        self.nome: str = nome
        self.escola: str = escola
        self.serie: str = serie
        self.turma_escola: str = turma_escola
        self.turno_escola: str = turno_escola
        self.data_cadastro: str = data_cadastro
        self.data_nasc: str = data_nasc
        self.endereco: str = endereco
        self.telefone: int = telefone
        self.filiacao: str = filiacao
        self.responsavel: str = responsavel
        self.beneficio: str = beneficio
        self.acompanhamento: str = acompanhamento
        self.orientacoes: str = orientacoes
        self.foto: str = foto
        self.status: int = 0  # 0 siginifica que o registro está ativo

    @classmethod
    def listar_alunos(cls, cursor):
        cursor.execute('SELECT * FROM ALUNO')

    def criar_aluno(self):
        query = (
            'INSERT INTO ALUNO (NOME, ESCOLA, SERIE, TURMA_ESCOLA, TURNO_ESCOLA, DATA_CADASTRO, DATA_NASC, ENDERECO,'
            ' TELEFONE, FILIACAO, RESPONSAVEL, BENEFICIO, ACOMPANHAMENTO, ORIENTACOES, FOTO, STATUS) VALUES '
            '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        values = (self.nome, self.escola, self.serie, self.turma_escola, self.turno_escola, self.data_cadastro,
                  self.data_nasc, self.endereco, self.telefone, self.filiacao, self.responsavel, self.beneficio,
                  self.acompanhamento, self.orientacoes, self.foto, self.status)

        return query, values

    @classmethod
    def deletar_aluno(cls, id: int):
        query = f'DELETE FROM student WHERE id = {id}'
        return query

    def desativar_aluno(self):
        pass
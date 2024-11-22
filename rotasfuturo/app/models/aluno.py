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

    @classmethod
    def selecionar_aluno(cls, id: int, cursor):
        query = '''
                SELECT ID_ALUNO, NOME, ESCOLA, SERIE, TURMA_ESCOLA, TURNO_ESCOLA, DATA_CADASTRO, DATA_NASC,
                       ENDERECO, TELEFONE, FILIACAO, RESPONSAVEL, BENEFICIO, ACOMPANHAMENTO, ORIENTACOES, FOTO, STATUS
                FROM ALUNO WHERE ID_ALUNO = %s
            '''
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            aluno = Aluno(result[1], result[2], result[3], result[4], result[5], result[6], result[7], result[8],
                          result[9], result[10], result[11], result[12], result[13], result[14], result[15])
            aluno.id = result[0]
            aluno.status = result[16]
            return aluno
        else:
            return None

    def criar_aluno(self):
        query = (
            'INSERT INTO ALUNO (NOME, ESCOLA, SERIE, TURMA_ESCOLA, TURNO_ESCOLA, DATA_CADASTRO, DATA_NASC, ENDERECO,'
            ' TELEFONE, FILIACAO, RESPONSAVEL, BENEFICIO, ACOMPANHAMENTO, ORIENTACOES, FOTO, STATUS) VALUES '
            '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)')
        values = (self.nome, self.escola, self.serie, self.turma_escola, self.turno_escola, self.data_cadastro,
                  self.data_nasc, self.endereco, self.telefone, self.filiacao, self.responsavel, self.beneficio,
                  self.acompanhamento, self.orientacoes, self.foto, self.status)

        return query, values

    def atualizar_aluno(self, id: int):
        query = '''
            UPDATE ALUNO 
            SET NOME = %s, ESCOLA = %s, SERIE = %s, TURMA_ESCOLA = %s, TURNO_ESCOLA = %s,
                DATA_CADASTRO = %s, DATA_NASC = %s, ENDERECO = %s, TELEFONE = %s, FILIACAO = %s, 
                RESPONSAVEL = %s, BENEFICIO = %s, ACOMPANHAMENTO = %s, ORIENTACOES = %s, FOTO = %s
            WHERE ID_ALUNO = %s
        '''
        values = (self.nome, self.escola, self.serie, self.turma_escola, self.turno_escola, self.data_cadastro,
                  self.data_nasc, self.endereco, self.telefone, self.filiacao, self.responsavel, self.beneficio,
                  self.acompanhamento, self.orientacoes, self.foto, id)

        return query, values

    @classmethod
    def deletar_aluno(cls, id: int):
        query = (f'DELETE FROM ALUNO WHERE ID_ALUNO = {id}')

        return query

    @classmethod
    def desativar_aluno(cls, id: int):
        query = (f'UPDATE ALUNO SET STATUS = 1 WHERE ID_ALUNO = {id}')

        return query

    @classmethod
    def ativar_aluno(cls, id: int):
        query = (f'UPDATE ALUNO SET STATUS = 0 WHERE ID_ALUNO = {id}')

        return query

    @classmethod
    def pesquisar(cls, pesquisa, cursor):
        query = "SELECT * FROM ALUNO WHERE NOME LIKE %s OR ID_ALUNO LIKE %s"
        cursor.execute(query, (f'%{pesquisa}%', f'%{pesquisa}%'))

class Visita:
    def __init__(self, id_aluno, data, objetivo,
    profissionais, familia, relato, conclusao):
        self.id_aluno: int = id_aluno
        self.data: str = data
        self.objetivo: str = objetivo
        self.profissionais: str = profissionais
        self.familia: str = familia
        self.relato: str = relato
        self.conclusao: str = conclusao

    @classmethod
    def listar_visitas(cls, cursor):
        cursor.execute('SELECT VISITA.ID_VISITA, ALUNO.NOME AS ALUNO_NOME, VISITA.DATA, '
                       'VISITA.OBJETIVO, VISITA.PROFISSIONAIS,'
                       ' VISITA.FAMILIA, VISITA.RELATO, VISITA.RELATO, VISITA.CONCLUSAO FROM VISITA JOIN ALUNO '
                       'ON VISITA.ID_ALUNO = ALUNO.ID_ALUNO')

    @classmethod
    def selecionar_visita(cls, id: int, cursor):
        query = '''
                    SELECT ID_VISITA, ID_ALUNO, DATA, OBJETIVO, PROFISSIONAIS, FAMILIA, RELATO, CONCLUSAO
                    FROM VISITA WHERE ID_VISITA = %s
                '''
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            visita = Visita(result[1], result[2], result[3], result[4], result[5], result[6],
                            result[7])
            visita.id = result[0]
            return visita
        else:
            return None

    def criar_visita(self):
        query = ('INSERT INTO VISITA (ID_ALUNO, DATA, OBJETIVO, PROFISSIONAIS, FAMILIA, RELATO,'
                 'CONCLUSAO ) VALUES (%s, %s, %s, %s, %s, %s, %s)')
        values = (self.id_aluno, self.data, self.objetivo, self.profissionais, self.familia, self.relato, self.conclusao)

        return query, values

    @classmethod
    def pesquisar(cls, pesquisa, cursor):
        query = "SELECT * FROM VISITA WHERE ID_VISITA LIKE %s OR ID_ALUNO LIKE %s OR DATA LIKE %s"
        cursor.execute(query, (f'%{pesquisa}%', f'%{pesquisa}%', f'%{pesquisa}%'))

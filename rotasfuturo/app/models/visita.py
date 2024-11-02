class Visita:
    def __init__(self, id_aluno, data, objetivo,
    profissionais, familia, escola_aluno, serie_aluno,
    relato, conclusao):
        self.id_aluno: int = id_aluno
        self.data: str = data
        self.objetivo: str = objetivo
        self.profissionais: str = profissionais
        self.familia: str = familia
        self.escola_aluno: str = escola_aluno
        self.serie_aluno: str = serie_aluno
        self.relato: str = relato
        self.conclusao: str = conclusao

    def criar_visita(self):
        query = ('INSERT INTO VISITA (ID_ALUNO, DATA, OBJETIVO, PROFISSIONAIS, FAMILIA, ESCOLA, SERIE, RELATO,'
                 'CONCLUSAO ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)')
        values = (self.id_aluno, self.data, self.objetivo, self.profissionais, self.familia, self.escola_aluno,
                  self.serie_aluno, self.relato, self.conclusao)

        return query, values

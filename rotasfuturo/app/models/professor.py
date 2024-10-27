class Professor:
    def __init__(self, nome, telefone, status):
        self.nome: str = nome
        self.telefone: int = telefone
        self.status: int = 0  # 0 siginifica que o registro está ativo

    def criar_professor(self):
        query = ('INSERT INTO PROFESSOR (NOME, TELEFONE, STATUS) VALUES (%s, %s, %s)')
        values = (self.nome, self.telefone, self.status)

        return query, values

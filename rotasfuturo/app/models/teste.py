class Teste:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade

    def create(self):
        query = 'INSERT INTO person (NAME, AGE) VALUES (%s, %s)'
        values = (self.nome, self.idade)

        return query, values

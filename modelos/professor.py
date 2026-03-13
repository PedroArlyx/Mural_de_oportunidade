from extensao import bd

class Professor(bd.Model):
    __tablename__ = 'professores'
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String)
    email = bd.Column(bd.String, unique=True)
    senha = bd.Column(bd.String)
    nome_projeto = bd.Column(bd.String)

    def __repr__(self):
        return f'<Nome: {self.nome}>'






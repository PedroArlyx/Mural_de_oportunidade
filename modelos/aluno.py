from extensao import bd

class Aluno(bd.Model):
    __tablename__ = 'alunos'
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String)
    email = bd.Column(bd.String, unique=True)
    senha = bd.Column(bd.String)
    id_professor = bd.Column(bd.Integer)

    def __repr__(self):
        return f'<Nome: {self.nome}, Email: {self.email}, id: {self.id}>'






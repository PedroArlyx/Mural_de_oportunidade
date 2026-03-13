#CRUD
from extensao import bd
from modelos.professor import Professor

class ProfessorDao:
    def __init__(self):
        self.bd = bd

    def verificar_login(self, email_usuario, senha_usuario):
        return Professor.query.filter_by(email=email_usuario, senha=senha_usuario).first()

    def cadastrar_professor(self, nome, email, senha, nome_projeto):
        professor = Professor(nome=nome, email=email, senha=senha, nome_projeto=nome_projeto)
        try:
            self.bd.session.add(professor)
            self.bd.session.commit()
            return True
        except Exception as e:
            print(e)
            self.bd.session.rollback()
            return False
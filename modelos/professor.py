from flask_login import LoginManager, UserMixin
from extensao import bd
from flask_login import UserMixin
from extensao import login_manager

@login_manager.user_loader 
def load_user(user_id):
    #eu carrego o usuario pelo id por meio do flask login
    return Professor.query.get(int(user_id))

class Professor(bd.Model, UserMixin):
    __tablename__ = 'professores'
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String)
    email = bd.Column(bd.String, unique=True)
    senha = bd.Column(bd.String)
    nome_projeto = bd.Column(bd.String)

    def __repr__(self):
        return f'<Nome: {self.nome}>'






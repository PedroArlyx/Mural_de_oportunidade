from extensao import bd
from extensao import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    user = bd.session.get(Usuario, int(user_id))
    if user:
        return user
    return bd.session.get(Administrador, int(user_id))

class Usuario(bd.Model, UserMixin):
   __tablename__='usuarios'

   id = bd.Column(bd.Integer,primary_key=True)
   nome=bd.Column(bd.String)
   email=bd.Column(bd.String, unique=True)
   senha_hash = bd.Column(bd.String(200))
   perfil=bd.Column(bd.String)
   bairro=bd.Column(bd.String)
   cidade=bd.Column(bd.String)
   media_avaliacao=bd.Column(bd.Float)
   criado_em=bd.Column(bd.DateTime,default=bd.func.now())

   def __repr__(self):
        return (f"Usuario(nome={self.nome}, email={self.email},perfil={self.perfil},bairro={self.bairro},"
                f"cidade={self.cidade},media_avaliacao={self.media_avaliacao},criado_em={self.criado_em}))")

class Administrador(bd.Model, UserMixin):
    __tablename__ = 'administradores'
    
    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(100), nullable=False)
    email = bd.Column(bd.String(100), unique=True, nullable=False)
    senha_hash = bd.Column(bd.String(255), nullable=False)
    perfil = bd.Column(bd.String)
    bairro = bd.Column(bd.String)
    cidade = bd.Column(bd.String)
    media_avaliacao = bd.Column(bd.Float)
    criado_em = bd.Column(bd.DateTime, default=bd.func.now())

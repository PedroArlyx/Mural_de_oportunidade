from extensao import bd
from flask_login import UserMixin

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

   @property
   def is_admin(self):
        return False

   def get_id(self):
       return str(self.id)
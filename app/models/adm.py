from app.extensao import bd
from app.extensao import login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_manager(user_id):
    return Adm.query.get(int(user_id))

class Adm(bd.Model, UserMixin):
   __tablename__='adm'

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
        return (f"Adm(nome={self.nome}, email={self.email},perfil={self.perfil},bairro={self.bairro},"
                f"cidade={self.cidade},media_avaliacao={self.media_avaliacao},criado_em={self.criado_em}))")

   @property
   def is_adm(self):
       return True

   def get_id(self):
       return f"adm_{self.id}"
#pedro@gmail.com
#senhar= 123
from extensao import bd
from flask_login import UserMixin

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

    def __repr__(self):
        return (f"Administrador(nome={self.nome}, email={self.email},perfil={self.perfil},bairro={self.bairro},"
                f"cidade={self.cidade},media_avaliacao={self.media_avaliacao},criado_em={self.criado_em}))")


    @property
    def is_admin(self):
        return True


    def get_id(self):
        return f"adm_{self.id}"
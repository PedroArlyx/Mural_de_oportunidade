from app.extensao import bd
from flask_login import UserMixin
from app.enums import *


class Usuario(bd.Model, UserMixin):
    __tablename__ = 'usuarios'

    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(100), nullable=False)
    email = bd.Column(bd.String, unique=True, nullable=False, index=True)
    senha_hash = bd.Column(bd.String(200))
    perfil = bd.Column(bd.Enum(Perfil), nullable=False, default=Perfil.USER)
    ativo = bd.Column(bd.Boolean, nullable=False, default=True)
    bairro = bd.Column(bd.String)
    cidade = bd.Column(bd.String)
    media_avaliacao = bd.Column(bd.Float, default=0.0)
    criado_em = bd.Column(bd.DateTime, default=bd.func.now())

    def __repr__(self):
        return f"<Usuario id={self.id} email={self.email}>"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "email": self.email,
            "perfil": self.perfil.value if hasattr(self.perfil, 'value') else self.perfil,
            "ativo": self.ativo,
            "bairro": self.bairro if self.bairro else None,
            "cidade": self.cidade if self.cidade else None,
            "media_avaliacao": float(self.media_avaliacao) if self.media_avaliacao is not None else 0.0,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }
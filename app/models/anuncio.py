from app.extensao import bd
from app.enums import *

class Anuncio(bd.Model):
    __tablename__ = 'anuncios'

    id=bd.Column(bd.Integer,primary_key=True)
    prestador_id=bd.Column(bd.Integer,bd.ForeignKey('usuarios.id', ondelete="CASCADE"),nullable=False,index=True)
    categoria_id=bd.Column(bd.Integer,bd.ForeignKey('categorias.id', ondelete="RESTRICT"),nullable=False,index=True)
    titulo=bd.Column(bd.String(100),nullable=False)
    descricao=bd.Column(bd.Text,nullable=False)
    preco=bd.Column(bd.Numeric(10,2),nullable=False)
    status=bd.Column(bd.Enum(StatusAnuncio),default=StatusAnuncio.ATIVO,nullable=False)
    criado_em=bd.Column(bd.DateTime,default=bd.func.now(),nullable=False)
    atualizado_em=bd.Column(bd.DateTime,default=bd.func.now(), onupdate=bd.func.now(), nullable=False)

    def __repr__(self):
        return f"<Anuncio id={self.id}, titulo={self.titulo}"

    def to_dict(self):
        return {
            "id": self.id,
            "prestador_id": self.prestador_id,
            "categoria_id": self.categoria_id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "preco": float(self.preco) if self.preco else None,
            "status": self.status.value if hasattr(self.status, 'value') else self.status,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None,
            "atualizado_em": self.atualizado_em.isoformat() if self.atualizado_em else None
        }

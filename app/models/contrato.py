from app.extensao import bd
from app.enums import StatusContrato


class Contrato(bd.Model):
    __tablename__ = 'contratos'

    id = bd.Column(bd.Integer, primary_key=True)
    cliente_id = bd.Column(bd.Integer, bd.ForeignKey('usuarios.id', ondelete='RESTRICT'), nullable=False, index=True)
    prestador_id = bd.Column(bd.Integer, bd.ForeignKey('usuarios.id', ondelete='RESTRICT'), nullable=False, index=True)
    anuncio_id = bd.Column(bd.Integer, bd.ForeignKey('anuncios.id', ondelete='RESTRICT'), nullable=False, index=True)
    assinado_em = bd.Column(bd.DateTime, default=bd.func.now(), nullable=False)
    valor_fechado = bd.Column(bd.Numeric(10,2), nullable=False)
    status = bd.Column(bd.Enum(StatusContrato), default=StatusContrato.PENDENTE, nullable=False, index=True)
    cliente = bd.relationship('Usuario', foreign_keys=[cliente_id],backref=bd.backref('contratos_como_cliente', lazy=True))
    prestador = bd.relationship('Usuario', foreign_keys=[prestador_id],backref=bd.backref('contratos_como_prestador', lazy=True))
    anuncio = bd.relationship('Anuncio', backref=bd.backref('contratos', lazy=True))

    def __repr__(self) -> str:
        return f"<Contrato id={self.id}  status={self.status} "

    def to_dict(self):

        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "prestador_id": self.prestador_id,
            "anuncio_id": self.anuncio_id,
            "assinado_em": self.assinado_em.isoformat() if self.assinado_em else None,
            "valor_fechado": float(self.valor_fechado) if self.valor_fechado else 0.0,
            "status": self.status.value if hasattr(self.status, 'value') else self.status
        }
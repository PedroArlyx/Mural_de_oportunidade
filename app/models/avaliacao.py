from app.extensao import bd


class Avaliacao(bd.Model):
    __tablename__ = 'avaliacoes'

    id = bd.Column(bd.Integer, primary_key=True)
    contrato_id = bd.Column(
        bd.Integer,
        bd.ForeignKey('contratos.id', ondelete='CASCADE'),
        unique=True,
        nullable=False,
        index=True
    )
    usuario_id = bd.Column(bd.Integer, bd.ForeignKey("usuarios.id"), nullable=False)
    nota = bd.Column(bd.Integer, nullable=False)
    comentario = bd.Column(bd.Text, nullable=True)
    criado_em = bd.Column(bd.DateTime, default=bd.func.now(), nullable=False)
    contrato = bd.relationship('Contrato', backref=bd.backref('avaliacao', uselist=False, lazy=True))
    usuario = bd.relationship("Usuario", backref=bd.backref("avaliacoes"))

    def __repr__(self) -> str:
        return f"<Avaliacao Id: {self.id}>"

    def to_dict(self) -> dict:

        return {
            "id": self.id,
            "contrato_id": self.contrato_id,
            "usuario_id": self.usuario_id,
            "nota": int(self.nota) if self.nota is not None else None,
            "comentario": self.comentario if self.comentario else None,
            "criado_em": self.criado_em.isoformat() if self.criado_em else None
        }
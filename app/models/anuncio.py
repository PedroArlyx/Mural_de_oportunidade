from app.extensao import bd

class Anuncio(bd.Model):
    __tablename__ = 'anuncio'

    id=bd.Column(bd.Integer,primary_key=True)
    prestador_id=bd.Column(bd.Integer,bd.ForeignKey('usuarios.id'))
    categoria_id=bd.Column(bd.Integer)
    titulo=bd.Column(bd.String)
    descricao=bd.Column(bd.String)
    preco=bd.Column(bd.Float)
    status=bd.Column(bd.String)
    criado_em=bd.Column(bd.DateTime,default=bd.func.now())
    atualizado_em=bd.Column(bd.DateTime,default=bd.func.now(), onupdate=bd.func.now())


    def __repr__ (self):
        return f"Anuncio(titulo={self.titulo}, descricao={self.descricao},preco{self.preco}, status={self.status},criado={self.criado_em}, atualizado={self.atualizado_em})"

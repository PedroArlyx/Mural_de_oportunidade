from app.extensao import bd

class Categoria(bd.Model):
    __tablename__ = 'categorias'

    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Categoria(id={self.id}, nome={self.nome})"

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
        }
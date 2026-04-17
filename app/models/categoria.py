from app.extensao import bd

class categoria(bd.Model):
    __tablename__ = 'categoria'

    id = bd.Column(bd.Integer)
    nome = bd.Column(bd.String)
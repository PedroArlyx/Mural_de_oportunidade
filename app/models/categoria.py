from extensao import bd

class categoria(bd.Model):
    __tablename__ = 'categoria'

    id = bd.Column(bd.Integer, primary_key=True)
    nome = bd.Column(bd.String)
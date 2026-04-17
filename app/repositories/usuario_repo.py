from app.extensao import bd
from app.models import Usuario


class UsuarioRepo:

    def salvar(self, usuario):
        bd.session.add(usuario)
        bd.session.commit()
        return usuario

    def buscar_por_email(self,email):
        return Usuario.query.filter_by(email=email).first()

    
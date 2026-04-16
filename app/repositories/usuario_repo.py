from extensao import bd
from app.models import Usuario


class UsuarioRepo:

    def salvar(self, usuario):
        bd.session.add(usuario)
        bd.session.commit()
        return usuario

    def buscar_por_email(self,email):
        return Usuario.query.filter_by(email=email).first()

    def buscar_por_id(selfself,id):
        return Usuario.query.get(id)
    def buscar_todos(self):
        return Usuario.query.all()
    def deletar(self,usuario):
        bd.session.delete(usuario)
        bd.session.commit()

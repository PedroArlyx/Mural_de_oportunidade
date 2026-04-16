from extensao import bd
from app.models import Administrador


class AdministradorRepo:

    def salvar(self, admin):
        bd.session.add(admin)
        bd.session.commit()
        return admin

    def buscar_por_email(self, email):
        return Administrador.query.filter_by(email=email).first()
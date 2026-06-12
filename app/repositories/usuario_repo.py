from app.extensao import bd
from app.models import Usuario
from typing import List, Optional


class UsuarioRepo:

    def salvar(self, usuario: Usuario) -> Usuario:
        try:
            bd.session.add(usuario)
            bd.session.commit()
            return usuario
        except Exception:
            bd.session.rollback()
            raise

    def buscar_por_id(self, id: int) -> Optional[Usuario]:
        return Usuario.query.get(id)

    def buscar_por_email(self, email: str) -> Optional[Usuario]:
        return Usuario.query.filter_by(email=email).first()

    def listar_todos(self) -> List[Usuario]:
        return Usuario.query.all()
    def deletar(self, usuario: Usuario) -> None:
        try:
            bd.session.delete(usuario)
            bd.session.commit()
        except Exception:
            bd.session.rollback()
            raise
    def listar_por_perfil(self, perfil: str) -> List[Usuario]:
        return Usuario.query.filter_by(perfil=perfil.strip().lower()).all()
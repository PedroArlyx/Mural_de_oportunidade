from app.models import Administrador
from app.repositories import  UsuarioRepo


class Adm_Service:
    def __init__(self):
        self.usuario_repo = UsuarioRepo()


    def listar_todos_usuarios(self):
        return self.usuario_repo.buscar_todos()

    def deletar_usuario(self,id):
        usuario = self.usuario_repo.buscar_por_id(id)

        if not usuario:
            return "usuario nao encontrado"

        self.usuario_repo.deletar(usuario)

        return "usuario deletado"






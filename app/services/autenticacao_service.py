from flask_jwt_extended import create_access_token
from app.repositories import UsuarioRepo
from app.Exceptions import UnauthorizedError, BadRequestError
from werkzeug.security import check_password_hash

class AutenticacaoService:
    def __init__(self):
        self.usuario_repository = UsuarioRepo()

    def autenticar(self, email, senha):

        if not email or not senha:
            raise BadRequestError("Email e senha sao obrigatorios")

        usuario = self.usuario_repository.buscar_por_email(email.lower().strip())

        if not usuario or not check_password_hash(usuario.senha_hash, senha):
            raise UnauthorizedError("E-mail ou senha Incorretos")
        if hasattr(usuario, "ativo") and not usuario.ativo:
            raise UnauthorizedError("Sua conta esta desativada")

        token = self.gerar_token(usuario.id)
        return token

    def gerar_token(self, usuario_id):
        return create_access_token(identity=str(usuario_id))


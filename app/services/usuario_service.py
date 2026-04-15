from app.models.usuario import Usuario
from app.repositories import UsuarioRepo
from werkzeug.security import generate_password_hash, check_password_hash


class UsuarioService:

    def __init__(self):
        self.UsuarioRepo = UsuarioRepo()

    def cadastrarUsuario(self, nome, email, senha, perfil, bairro, cidade):
        usuario_existente = self.UsuarioRepo.buscar_por_email(email)

        if usuario_existente:
            return None

        senha_hash = generate_password_hash(senha)

        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            perfil=perfil,
            bairro=bairro,
            cidade=cidade
        )

        return self.UsuarioRepo.salvar(usuario)

    def login(self, email,senha):
        usuario = self.UsuarioRepo.buscar_por_email(email)

        if not usuario:
            return None

        if not check_password_hash(usuario.senha_hash, senha):
            return None

        return usuario
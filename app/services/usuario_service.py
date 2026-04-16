from app.models.usuario import Usuario
from app.repositories import UsuarioRepo
from werkzeug.security import generate_password_hash, check_password_hash


class UsuarioService:

    def __init__(self):
        self.Usuario_repo = UsuarioRepo()

    def cadastrar_usuario(self, nome, email, senha, perfil, bairro, cidade):
        if not nome or not email or not senha:
            return "dados Invalidos"

        if len(senha) <6:
            return "senha muito curta"

        usuario_existente = self.Usuario_repo.buscar_por_email(email)

        if usuario_existente:
            return "email ja cadastrado"

        senha_hash = generate_password_hash(senha)

        usuario = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            perfil=perfil,
            bairro=bairro,
            cidade=cidade
        )

        return self.Usuario_repo.salvar(usuario)

    def login(self, email,senha):
        usuario = self.Usuario_repo.buscar_por_email(email)

        if not usuario:
            return "usuario nao encontrado"

        if not check_password_hash(usuario.senha_hash, senha):
            return "senha incorreto"

        return usuario
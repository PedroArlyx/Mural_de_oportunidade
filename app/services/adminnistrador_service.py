from app.repositories import AdministradorRepo
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import Administrador


class AdministradorService:

    def __init__(self):
        self.admin_repo = AdministradorRepo()

    def cadastrar_admin(self, nome, email, senha):

        if not nome or not email or not senha:
            return "dados invalidos"

        admin_existente = self.admin_repo.buscar_por_email(email)

        if admin_existente:
            return "email ja cadastrado"

        senha_hash = generate_password_hash(senha)

        admin = Administrador(
            nome=nome,
            email=email,
            senha_hash=senha_hash
        )

        return self.admin_repo.salvar(admin)

    def login_admin(self, email, senha):
        admin = self.admin_repo.buscar_por_email(email)

        if not admin:
            return "admin nao encontrado"

        if not check_password_hash(admin.senha_hash, senha):
            return "senha incorreta"

        return admin
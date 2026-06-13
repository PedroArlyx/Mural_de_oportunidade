import re
from typing import List
from werkzeug.security import check_password_hash, generate_password_hash
from app.Exceptions import BadRequestError, ConflictError, NotFoundError, UnauthorizedError
from app.enums import Perfil
from app.models.usuario import Usuario
from app.repositories.usuario_repo import UsuarioRepo

_EMAIL_REGEX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")


class UsuarioService:

    def __init__(self):
        self._repo = UsuarioRepo()

    def cadastrar(self, nome: str, email: str, senha: str, perfil: str,numero: int, bairro: str, cidade: str) -> Usuario:
        self._validar_campos_obrigatorios(nome=nome, email=email, senha=senha,numero=numero ,perfil=perfil, bairro=bairro,cidade=cidade)
        self._validar_email(email)

        email = email.lower().strip()
        self._garantir_email_unico(email)

        perfil_enum = self._converter_perfil(perfil)

        usuario = Usuario(
            nome=nome.strip(),
            email=email,
            senha_hash=generate_password_hash(senha),
            perfil=perfil_enum,
            numero=numero,
            bairro=bairro.strip(),
            cidade=cidade.strip(),
        )
        return self._repo.salvar(usuario)

    def buscar_por_id(self, usuario_id: int) -> Usuario:
        usuario = self._repo.buscar_por_id(usuario_id)
        if not usuario:
            raise NotFoundError("Usuário não encontrado.")
        return usuario

    def listar_todos(self,solicitante_id) -> List[Usuario]:
        self._exigir_perfil_admin(solicitante_id)
        return self._repo.listar_todos()

    def atualizar(self, usuario_id: int, nome: str, email: str,numero: str,bairro:str,cidade:str) -> Usuario:
        usuario = self.buscar_por_id(usuario_id)

        self._validar_email(email)
        email = email.lower().strip()

        if usuario.email != email:
            self._garantir_email_unico(email)
        usuario.nome = nome.strip()
        usuario.email = email.strip()
        usuario.numero = numero
        usuario.bairro = bairro
        usuario.cidade = cidade
        return self._repo.salvar(usuario)

    def deletar(self,usuario_id:int )-> List[Usuario]:
        usuario = self.buscar_por_id(usuario_id)
        self._repo.deletar(usuario)

    def _validar_campos_obrigatorios(self, **campos) -> None:
        nomes_pt = {
            "nome": "nome", "email": "e-mail", "senha": "senha","numero": "numero",
            "perfil": "perfil", "bairro": "bairro", "cidade": "cidade",
        }
        for campo, valor in campos.items():
            if not valor or not str(valor).strip():
                raise BadRequestError(f"O campo '{nomes_pt.get(campo, campo)}' é obrigatório.")

    def _validar_email(self, email: str) -> None:
        if not _EMAIL_REGEX.match(email):
            raise BadRequestError("Formato de e-mail inválido.")

    def _garantir_email_unico(self, email: str) -> None:
        if self._repo.buscar_por_email(email):
            raise ConflictError("Este e-mail já está cadastrado.")

    def listar_usuarios_por_perfil_adm(self, solicitante_id: int, perfil_alvo: str) -> List[Usuario]:

        self._exigir_perfil_admin(solicitante_id)
        return self._repo.listar_por_perfil(perfil_alvo)

    def alternar_status_usuario_adm(self, solicitante_id: int, usuario_id: int, ativo: bool) -> Usuario:

        self._exigir_perfil_admin(solicitante_id)

        if solicitante_id == usuario_id:
            raise BadRequestError("Um administrador não pode desativar a própria conta.")

        usuario = self.buscar_por_id(usuario_id)
        usuario.ativo = ativo
        return self._repo.salvar(usuario)

    def alterar_perfil_usuario_adm(self, solicitante_id: int, usuario_id: int, novo_perfil: str) -> Usuario:

        if not novo_perfil or not novo_perfil.strip():
            raise BadRequestError("O novo perfil deve ser informado.")

        self._exigir_perfil_admin(solicitante_id)

        perfil_enum = self._converter_perfil(novo_perfil)

        usuario = self.buscar_por_id(usuario_id)
        usuario.perfil = perfil_enum
        return self._repo.salvar(usuario)

    def _exigir_perfil_admin(self, usuario_id: int) -> None:

        usuario_solicitante = self.buscar_por_id(usuario_id)

        if usuario_solicitante.perfil.value.upper().strip() != "ADMIN":
            raise UnauthorizedError("Acesso negado. Esta operação é exclusiva para administradores.")

    def Blacklist_ou_Deletar_usuario_adm(self, solicitante_id: int, usuario_id: int) -> None:

        self._exigir_perfil_admin(solicitante_id)

        if solicitante_id == usuario_id:
            raise BadRequestError("Um administrador não pode deletar a própria conta por este método.")

        usuario = self.buscar_por_id(usuario_id)
        self._repo.deletar(usuario)
    def _converter_perfil(self,perfil: str) -> Perfil:
        try:
            return Perfil[perfil.strip().upper()]
        except(KeyError,AttributeError):
            valores =[p.value for p in Perfil]
            raise BadRequestError (f"Perfil invalido. valores aceitos: {valores}")


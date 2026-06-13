from typing import List
from app.models.categoria import Categoria
from app.repositories import CategoriaRepo
from app.services.usuario_service import UsuarioService
from app.Exceptions import BadRequestError, ConflictError, NotFoundError


class CategoriaService:

    def __init__(self):
        self._repo = CategoriaRepo()
        self._usuario_service = UsuarioService()

    def cadastrar_por_adm(self, solicitante_id: int, nome: str) -> Categoria:
        self._exigir_perfil_admin(solicitante_id)
        if not nome or not nome.strip():
            raise BadRequestError("O nome da categoria é obrigatório.")
        nome_limpo = nome.strip()
        if self._repo.buscar_por_nome(nome_limpo):
            raise ConflictError(f"A categoria '{nome_limpo}' já está cadastrada.")
        try:
            return self._repo.criar(nome_limpo)
        except Exception as exc:
            raise Exception(str(exc))

    def buscar_por_id(self, categoria_id: int) -> Categoria:
        try:
            categoria = self._repo.buscar_por_id(categoria_id)
        except Exception as exc:
            raise BadRequestError(str(exc))
        if not categoria:
            raise NotFoundError("Categoria não encontrada.")
        return categoria

    def listar_todas(self) -> List[Categoria]:
        try:
            return self._repo.listar_todas()
        except Exception as exc:
            raise Exception(str(exc))

    def atualizar_por_adm(self, solicitante_id: int, categoria_id: int, novo_nome: str) -> Categoria:
        self._exigir_perfil_admin(solicitante_id)
        if not novo_nome or not novo_nome.strip():
            raise BadRequestError("O novo nome da categoria é obrigatório.")
        novo_nome_limpo = novo_nome.strip()
        categoria = self.buscar_por_id(categoria_id)
        if categoria.nome.lower() != novo_nome_limpo.lower():
            if self._repo.buscar_por_nome(novo_nome_limpo):
                raise ConflictError(f"Já existe outra categoria com o nome '{novo_nome_limpo}'.")
        try:
            return self._repo.atualizar(categoria_id, novo_nome_limpo)
        except Exception as exc:
            raise Exception(str(exc))

    def deletar_por_adm(self, solicitante_id: int, categoria_id: int) -> None:
        self._exigir_perfil_admin(solicitante_id)
        self.buscar_por_id(categoria_id)
        try:
            self._repo.deletar(categoria_id)
        except Exception as exc:
            raise Exception(
                f"Não é possível deletar esta categoria pois ela possui anúncios s. Detalhes: {str(exc)}"
            )

    def _exigir_perfil_admin(self, usuario_id: int) -> None:
        self._usuario_service._exigir_perfil_admin(usuario_id)
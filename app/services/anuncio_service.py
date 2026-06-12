from typing import List
from app.Exceptions import BadRequestError, ForbiddenError, NotFoundError
from app.models import Anuncio
from app.repositories import AnuncioRepo


class AnuncioService:

    def __init__(self):
        self._repo = AnuncioRepo()

    def criar(self, prestador_id: int, categoria_id: int, titulo: str, descricao: str, preco: float) -> Anuncio:
        self._validar_dados(titulo, descricao, preco)
        anuncio = Anuncio(
            prestador_id=prestador_id,
            categoria_id=categoria_id,
            titulo=titulo.strip(),
            descricao=descricao.strip(),
            preco=preco,
        )
        return self._repo.salvar_anuncio(anuncio)

    def listar(self) -> List[Anuncio]:
        return self._repo.listar_todos_anuncios()

    def buscar_por_id(self, anuncio_id: int) -> Anuncio:
        anuncio = self._repo.buscar_por_id(anuncio_id)
        if not anuncio:
            raise NotFoundError("Anúncio não encontrado.")
        return anuncio

    def atualizar(self, anuncio_id: int, usuario_id: int, titulo: str, descricao: str, preco: float,categoria_id: int) -> Anuncio:
        anuncio = self.buscar_por_id(anuncio_id)
        self._verificar_permissao(anuncio, usuario_id)
        self._validar_dados(titulo, descricao, preco)

        anuncio.titulo = titulo.strip()
        anuncio.descricao = descricao.strip()
        anuncio.preco = preco
        anuncio.categoria_id = categoria_id
        return self._repo.salvar_anuncio(anuncio)

    def deletar(self, anuncio_id: int, usuario_id: int) -> None:
        anuncio = self.buscar_por_id(anuncio_id)
        self._verificar_permissao(anuncio, usuario_id)
        self._repo.deletar_anuncio(anuncio)

    def _validar_dados(self, titulo: str, descricao: str, preco: float) -> None:
        if not titulo or not titulo.strip():
            raise BadRequestError("O título é obrigatório.")
        if not descricao or not descricao.strip():
            raise BadRequestError("A descrição é obrigatória.")
        if preco is None or float(preco) < 0:
            raise BadRequestError("O preço não pode ser negativo.")

    def _verificar_permissao(self, anuncio: Anuncio, usuario_id: int) -> None:
        if anuncio.prestador_id != usuario_id:
            raise ForbiddenError("Você não tem permissão para modificar este anúncio.")
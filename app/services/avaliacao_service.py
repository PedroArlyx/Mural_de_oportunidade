from typing import List
from app.Exceptions import NotFoundError, ForbiddenError
from app.models import Avaliacao
from app.repositories import AvaliacaoRepo


class AvaliacaoService:

    def __init__(self):
        self._repo = AvaliacaoRepo()

    def criar(self,contrato_id:int,usuario_id,nota:int,comentario:str) -> Avaliacao:
        avaliacao = Avaliacao(contrato_id=contrato_id,usuario_id=usuario_id,nota=nota,comentario=comentario.strip())
        return self._repo.salvar(avaliacao)

    def listar_todas_avaliacao(self) -> List[Avaliacao]:
        return self._repo.listar_todas_avaliacao()

    def buscar_por_id(self, avaliacao_id: int) -> Avaliacao:
        avaliacao = self._repo.buscar_por_id(avaliacao_id)
        if not avaliacao:
            raise NotFoundError("Avaiacao não encontrada.")
        return avaliacao
    def atualizar(self,avaliacao_id:int,nota:int,comentario:str) -> Avaliacao:
        avaliacao = self._repo.buscar_por_id(avaliacao_id)
        avaliacao.nota = nota
        avaliacao.comentario = comentario
        return self._repo.atualizar(avaliacao)
    def deletar(self,avaliacao_id:int, usuario_id: int) -> Avaliacao:
        avaliacao = self._repo.buscar_por_id(avaliacao_id)
        self._verificar_permissao(avaliacao, usuario_id)
        self._repo.deletar(avaliacao)

    def _verificar_permissao(self, avaliacao: Avaliacao, usuario_id: int) -> None:
        if avaliacao.usuario_id != usuario_id:
            raise ForbiddenError("Você não tem permissão para modificar este anúncio.")
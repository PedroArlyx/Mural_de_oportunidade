from typing import List,Optional
from app.models import Avaliacao
from app.extensao import bd


class AvaliacaoRepo:

    def salvar(self, avaliacao:  Avaliacao) -> Avaliacao:
        try:
            bd.session.add(avaliacao)
            bd.session.commit()
            return avaliacao
        except Exception  :
            bd.session.rollback()
            raise
    def deletar(self, avaliacao: Avaliacao) -> Avaliacao:
        try:
            bd.session.delete(avaliacao)
            bd.session.commit()
        except Exception :
            bd.session.rollback()
            raise

    def atualizar(self, avaliacao: Avaliacao) -> Avaliacao:
        try:
            bd.session.add(avaliacao)
            bd.session.commit()
            return avaliacao
        except Exception :
            bd.session.rollback()
            raise

    def listar_todas_avaliacao(self) -> List[Avaliacao]:
        return Avaliacao.query.all()

    def buscar_por_id(self, id: int) -> Optional[Avaliacao]:
        return Avaliacao.query.get(id)
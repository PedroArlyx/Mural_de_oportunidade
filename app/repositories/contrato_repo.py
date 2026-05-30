from typing import List, Optional
from app.extensao import bd
from app.models import Contrato


class ContratoRepo:

    def criarContrato(self, contrato: Contrato) -> Contrato:
        try:
            bd.session.add(contrato)
            bd.session.commit()
            return contrato
        except Exception:
            bd.session.rollback()
            raise

    def buscar_por_id(self, id: int) -> Optional[Contrato]:
        return bd.session.get(Contrato,id)

    def listar_todos(self) -> List[Contrato]:
        return Contrato.query.all()

    def listar_por_cliente(self, cliente_id: int) -> List[Contrato]:
        return Contrato.query.filter_by(cliente_id=cliente_id).all()

    def listar_por_prestador(self, prestador_id: int) -> List[Contrato]:
        return Contrato.query.filter_by(prestador_id=prestador_id).all()

    def atualizar(self, contrato: Contrato) -> Contrato:
        try:
            bd.session.add(contrato)
            bd.session.commit()
            return contrato
        except Exception:
            bd.session.rollback()
            raise

    def deletar(self, contrato: Contrato) -> None:
        try:
            bd.session.delete(contrato)
            bd.session.commit()
        except Exception:
            bd.session.rollback()
            raise

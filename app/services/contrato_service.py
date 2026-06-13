from typing import List
from app.enums import StatusContrato
from app.models import Contrato
from app.repositories import ContratoRepo
from app.services import UsuarioService
from app.Exceptions import BadRequestError, NotFoundError, UnauthorizedError


class ContratoService:

    def __init__(self):
        self._repo = ContratoRepo()
        self._usuario_service = UsuarioService()

    def criar(self, cliente_id: int, prestador_id: int, anuncio_id: int, valor_fechado: float) -> Contrato:

        if not valor_fechado or float(valor_fechado) <= 0:
            raise BadRequestError("O valor fechado do contrato deve ser maior que zero.")

        if cliente_id == prestador_id:
            raise BadRequestError("Um cliente não pode abrir um contrato com ele mesmo.")

        self._usuario_service.buscar_por_id(cliente_id)
        self._usuario_service.buscar_por_id(prestador_id)

        novo_contrato = Contrato(
            cliente_id=cliente_id,
            prestador_id=prestador_id,
            anuncio_id=anuncio_id,
            valor_fechado=valor_fechado,
            status=StatusContrato.PENDENTE
        )
        return self._repo.criarContrato(novo_contrato)

    def buscar_por_id(self, solicitante_id: int, contrato_id: int) -> Contrato:

        contrato = self._repo.buscar_por_id(contrato_id)

        if not contrato:
            raise NotFoundError("Contrato não encontrado.")

        if not self._usuario_eh_envolvido_ou_adm(solicitante_id, contrato):
            raise UnauthorizedError("Acesso negado. Você não tem permissão para visualizar este contrato.")

        return contrato

    def listar_por_usuario(self, solicitante_id: int, usuario_alvo_id: int) -> List[Contrato]:

        if solicitante_id != usuario_alvo_id:
            self._exigir_perfil_admin(solicitante_id)

        contratos_cliente = self._repo.listar_por_cliente(usuario_alvo_id)
        contratos_prestador = self._repo.listar_por_prestador(usuario_alvo_id)

        return contratos_cliente + contratos_prestador

    def atualizar_status(self, solicitante_id: int, contrato_id: int, novo_status_str: str) -> Contrato:
        contrato = self.buscar_por_id(solicitante_id, contrato_id)

        mapeamento = {
            "pendente": StatusContrato.PENDENTE,
            "ativo": StatusContrato.ATIVO,
            "concluido": StatusContrato.CONCLUIDO,
            "cancelado": StatusContrato.CANCELADO,
            "restrito": StatusContrato.RESTRITO
        }

        status_enum = mapeamento.get(novo_status_str.strip().lower())
        if not status_enum:
            raise BadRequestError(f"Status '{novo_status_str}' inválido para transição.")

        contrato.status = status_enum
        return self._repo.atualizar(contrato)

    def deletar_por_adm(self, solicitante_id: int, contrato_id: int) -> None:

        self._exigir_perfil_admin(solicitante_id)

        contrato = self._repo.buscar_por_id(contrato_id)
        if not contrato:
            raise NotFoundError("Contrato não encontrado.")

        self._repo.deletar(contrato)


    def _usuario_eh_envolvido_ou_adm(self, usuario_id: int, contrato: Contrato) -> bool:
        if usuario_id in [contrato.cliente_id, contrato.prestador_id]:
            return True

        try:
            self._exigir_perfil_admin(usuario_id)
            return True
        except UnauthorizedError:
            return False

    def _exigir_perfil_admin(self, usuario_id: int) -> None:
        self._usuario_service._exigir_perfil_admin(usuario_id)



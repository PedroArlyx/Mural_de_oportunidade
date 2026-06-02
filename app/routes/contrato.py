import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.Exceptions import AppError
from app.services import ContratoService

logger = logging.getLogger(__name__)
bp_contratos = Blueprint("contratos", __name__, url_prefix="/contratos")
_service = ContratoService()


@bp_contratos.route("", methods=["POST"])
@jwt_required()
def criar():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), HTTPStatus.BAD_REQUEST

    try:

        cliente_id_logado = int(get_jwt_identity())

        contrato = _service.criar(
            cliente_id=cliente_id_logado,
            prestador_id=payload.get("prestador_id"),
            anuncio_id=payload.get("anuncio_id"),
            valor_fechado=payload.get("valor_fechado")
        )

        return jsonify(contrato.to_dict()), HTTPStatus.CREATED

    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao criar contrato: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_contratos.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar(id: int):
    try:
        solicitante_id = int(get_jwt_identity())
        contrato = _service.buscar_por_id(solicitante_id=solicitante_id, contrato_id=id)
        return jsonify(contrato.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao buscar contrato: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_contratos.route("/<int:id>/status", methods=["PATCH"])
@jwt_required()
def mudar_status(id: int):
    payload = request.get_json(silent=True) or {}
    novo_status = payload.get("status")

    if not novo_status:
        return jsonify({"erro": "O campo 'status' (string) é obrigatório."}), HTTPStatus.BAD_REQUEST

    try:
        solicitante_id = int(get_jwt_identity())
        contrato = _service.atualizar_status(
            solicitante_id=solicitante_id,
            contrato_id=id,
            novo_status_str=novo_status
        )
        return jsonify(contrato.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao modificar status do contrato: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_contratos.route("", methods=["GET"])
@jwt_required()
def listar():
    try:
        usuario_logado_id = int(get_jwt_identity())
        contratos = _service.listar_por_usuario(
            solicitante_id=usuario_logado_id,
            usuario_alvo_id=usuario_logado_id
        )
        return jsonify([c.to_dict() for c in contratos]), HTTPStatus.OK

    except Exception as exc:
        logger.error("Erro ao listar contratos do usuário: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR
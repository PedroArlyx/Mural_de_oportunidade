import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.Exceptions import AppError
from app.services import AvaliacaoService
from app.middlewares import autorizacao_adm

logger = logging.getLogger(__name__)
bp_avaliacao = Blueprint("avaliacao", __name__, url_prefix="/avaliacao")
_avaliacao_service = AvaliacaoService()


@bp_avaliacao.route("", methods=["GET"])
@jwt_required()
def listar():

    try:
        avaliacoes = _avaliacao_service.listar_todas_avaliacao()

        return jsonify([c.to_dict() for c in avaliacoes]), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao listar avaliacoes: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_avaliacao.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar(id: int):

    try:
        avaliacao = _avaliacao_service.buscar_por_id(avaliacao_id=id)
        return jsonify(avaliacao.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao buscar avaliacoes: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_avaliacao.route("", methods=["POST"])
@jwt_required()
def criar():

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), HTTPStatus.BAD_REQUEST

    try:

        usuario_id = int(get_jwt_identity())

        nova_avaliacao = _avaliacao_service.criar(usuario_id=usuario_id, **payload)
        return jsonify({"id": nova_avaliacao.id,"comentario": nova_avaliacao.comentario, "notA" : nova_avaliacao.nota}), HTTPStatus.CREATED
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao criar avaliacao %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_avaliacao.route("/<int:id>", methods=["PUT"])
@jwt_required()
@autorizacao_adm(permitir_proprio=True)
def atualizar(id: int):

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), HTTPStatus.BAD_REQUEST

    try:
        solicitante_id = int(get_jwt_identity())

        avaliacao_atualizada = _avaliacao_service.atualizar(avaliacao_id=id, **payload)
        return jsonify(avaliacao_atualizada.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao atualizar categoria pelo ADM: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_avaliacao.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@autorizacao_adm(permitir_proprio=True)
def deletar(id: int):

    try:
        solicitante_id = int(get_jwt_identity())

        _avaliacao_service.deletar(avaliacao_id=id,solicitante_id=solicitante_id)
        return "", HTTPStatus.NO_CONTENT
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao deletar avaliacao %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR
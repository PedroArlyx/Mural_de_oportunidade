import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.Exceptions import AppError
from app.services.categoria_service import CategoriaService

logger = logging.getLogger(__name__)
bp_categorias = Blueprint("categorias", __name__, url_prefix="/categorias")
_categoria_service = CategoriaService()


@bp_categorias.route("", methods=["GET"])
@jwt_required()
def listar():

    try:
        categorias = _categoria_service.listar_todas()

        return jsonify([c.to_dict() for c in categorias]), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao listar categorias: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_categorias.route("/<int:id>", methods=["GET"])
@jwt_required()
def buscar(id: int):

    try:
        categoria = _categoria_service.buscar_por_id(categoria_id=id)
        return jsonify(categoria.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao buscar categoria: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_categorias.route("", methods=["POST"])
@jwt_required()
def criar():

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), HTTPStatus.BAD_REQUEST

    try:

        solicitante_id = int(get_jwt_identity())

        nova_categoria = _categoria_service.cadastrar_por_adm(
            solicitante_id=solicitante_id,
            nome=payload.get("nome")
        )
        return jsonify({"id": nova_categoria.id,"nome": nova_categoria.nome}), HTTPStatus.CREATED
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao criar categoria pelo ADM: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_categorias.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar(id: int):

    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), HTTPStatus.BAD_REQUEST

    try:
        solicitante_id = int(get_jwt_identity())

        categoria_atualizada = _categoria_service.atualizar_por_adm(
            solicitante_id=solicitante_id,
            categoria_id=id,
            novo_nome=payload.get("nome")
        )
        return jsonify(categoria_atualizada.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao atualizar categoria pelo ADM: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_categorias.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def deletar(id: int):

    try:
        solicitante_id = int(get_jwt_identity())

        _categoria_service.deletar_por_adm(
            solicitante_id=solicitante_id,
            categoria_id=id
        )
        return "", HTTPStatus.NO_CONTENT
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro operacional ao deletar categoria pelo ADM: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR
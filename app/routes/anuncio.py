import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.Exceptions import AppError
from app.services.anuncio_service import AnuncioService

logger = logging.getLogger(__name__)
bp_anuncios = Blueprint("anuncios", __name__, url_prefix="/anuncios")
_service = AnuncioService()


@bp_anuncios.route("", methods=["POST"])
@jwt_required()
def criar():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), HTTPStatus.BAD_REQUEST

    preco_raw = payload.get("preco")
    try:
        preco = float(preco_raw)
    except (TypeError, ValueError):
        return jsonify({"erro": "O preço deve ser um valor numérico."}), HTTPStatus.BAD_REQUEST

    try:
        usuario_id = int(get_jwt_identity())
        anuncio = _service.criar(
            prestador_id=usuario_id,
            categoria_id=payload.get("categoria_id"),
            titulo=payload.get("titulo"),
            descricao=payload.get("descricao"),
            preco=preco,
        )
        return jsonify(anuncio.to_dict()), HTTPStatus.CREATED
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro ao criar anúncio: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_anuncios.route("", methods=["GET"])
def listar():
    try:
        anuncios = _service.listar()
        return jsonify([a.to_dict() for a in anuncios]), HTTPStatus.OK
    except Exception as exc:
        logger.error("Erro ao listar anúncios: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_anuncios.route("/<int:id>", methods=["GET"])
def buscar(id: int):
    try:
        anuncio = _service.buscar_por_id(id)
        return jsonify(anuncio.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code


@bp_anuncios.route("/<int:id>", methods=["PUT"])
@jwt_required()
def atualizar(id: int):
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), HTTPStatus.BAD_REQUEST

    preco_raw = payload.get("preco")
    try:
        preco = float(preco_raw)
    except (TypeError, ValueError):
        return jsonify({"erro": "O preço deve ser um valor numérico."}), HTTPStatus.BAD_REQUEST

    try:
        usuario_id = int(get_jwt_identity())
        anuncio = _service.atualizar(
            anuncio_id=id,
            usuario_id=usuario_id,
            titulo=payload.get("titulo"),
            descricao=payload.get("descricao"),
            preco=preco,
        )
        return jsonify(anuncio.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro ao atualizar anúncio: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_anuncios.route("/<int:id>", methods=["DELETE"])
@jwt_required()

def deletar(id: int):
    try:
        usuario_id = int(get_jwt_identity())
        _service.deletar(anuncio_id=id, usuario_id=usuario_id)
        return "", HTTPStatus.NO_CONTENT
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code

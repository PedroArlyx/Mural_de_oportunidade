import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request

from app.Exceptions import AppError
from app.services import AutenticacaoService

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
_auth_service = AutenticacaoService()


def _error_response(type: str, mensagem: str) -> dict:
    return {"status": "error", "type": type, "mensagem": mensagem}


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True)

    if not payload:
        return (
            jsonify(_error_response("BadRequest", "O formato da requisição deve ser JSON.")),
            HTTPStatus.BAD_REQUEST,
        )

    email = payload.get("email")
    senha = payload.get("senha")

    if not email or not senha:
        return (
            jsonify(_error_response("BadRequest", "E-mail e senha são obrigatórios.")),
            HTTPStatus.BAD_REQUEST,
        )

    try:
        token = _auth_service.autenticar(email=email, senha=senha)
    except AppError as exc:
        logger.error("Erro interno na autenticação: %s", exc, exc_info=True)
        return (
            jsonify(_error_response("InternalServerError", "Ocorreu um erro interno no servidor.")),
            HTTPStatus.INTERNAL_SERVER_ERROR,
        )

    return (
        jsonify({"status": "success", "data": {"access_token": token, "token_type": "Bearer"}}),
        HTTPStatus.OK,
    )

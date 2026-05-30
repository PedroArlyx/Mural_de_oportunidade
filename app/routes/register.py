import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request

from app.Exceptions import AppError
from app.services import UsuarioService

logger= logging.getLogger(__name__)
bp_register = Blueprint("register", __name__, url_prefix="/register")
_service = UsuarioService()


def _build_user_response(usuario, nome: str, email: str, perfil: str) -> dict:
    return {
        "mensagem": "Usuário cadastrado com sucesso.",
        "usuario": {
            "id": getattr(usuario, "id", None),
            "nome": nome,
            "email": email,
            "perfil": perfil,
        },
    }


@bp_register.route("", methods=["POST"])
def register():
    payload = request.get_json(silent=True)

    if not payload:
        return (
            jsonify({"erro": "Corpo da requisição vazio ou formato inválido (deve ser JSON)."}),
            HTTPStatus.BAD_REQUEST,
        )

    nome = payload.get("nome")
    email = payload.get("email")
    senha = payload.get("senha")
    perfil = payload.get("perfil")
    bairro = payload.get("bairro")
    cidade = payload.get("cidade")

    try:
        usuario = _service.cadastrar(nome, email, senha, perfil, bairro, cidade)
    except AppError as exc:
        return jsonify({"erro": exc.menssagem}),exc.status_code
    except Exception as exc:
        logger.error("erro interno ao cadrastra usuario: %s",exc, exc_info=True)
        return jsonify({"erro":"Erro interno no servidor"}), HTTPStatus.INTERNAL_SERVER_ERROR

    if usuario is None:
        return (
            jsonify({"erro": "E-mail já cadastrado no sistema."}),
            HTTPStatus.CONFLICT,
        )

    return (
        jsonify(_build_user_response(usuario, nome, email, perfil)),
        HTTPStatus.CREATED,
    )

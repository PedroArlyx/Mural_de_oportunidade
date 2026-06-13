import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from app.Exceptions import AppError, UnauthorizedError
from app.services import AutenticacaoService
from app.services import UsuarioService

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__, url_prefix="/auth")
_auth_service = AutenticacaoService()
_UsuarioService = UsuarioService()


@auth_bp.route("/register", methods=["POST"])
def register():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "o corpo da requisicao deve ser JSON"}), HTTPStatus.BAD_REQUEST

    try:
        usuario = _UsuarioService.cadastrar(nome=payload.get("nome"),
                                            email=payload.get("email"),
                                            senha=payload.get("senha"),
                                            perfil="USER",
                                            numero=payload.get("numero"),
                                            bairro=payload.get("bairro"),
                                            cidade=payload.get("cidade"),
                                            )
    except AppError as exc:
        return jsonify(exc.to_dict()), exc.status_code
    except Exception as exc:
        logger.error(f"erro interno ao cadrastra usuario: %s", exc, exc_info=True)
        return jsonify({"erro": "erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR

    return jsonify(usuario.to_dict()), HTTPStatus.CREATED


@auth_bp.route("/login", methods=["POST"])
def login():
    payload = request.get_json(silent=True)

    if not payload:
        return jsonify({"erro": "o corpo da requisicao deve ser JSON"}), HTTPStatus.BAD_REQUEST
    email = payload.get("email")
    senha = payload.get("senha")

    if not email or not senha:
        return jsonify({"erro": "E-mail é senha sao obrigratorios"}), HTTPStatus.BAD_REQUEST,

    try:
        token = _auth_service.autenticar(email=email, senha=senha)
    except UnauthorizedError as exc:
        logger.error("Erro interno na autenticação: %s", exc, exc_info=True)
        return jsonify({"erro": exc.mensagem}), exc.status_code

    return jsonify({"status": "success", "data": {"access_token": token, "token_type": "Bearer"}}), HTTPStatus.OK,

import logging
from http import HTTPStatus
from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.Exceptions import AppError
from app.services import UsuarioService
from app.middlewares import autorizacao_adm

logger = logging.getLogger(__name__)
bp_adm = Blueprint("adm", __name__, url_prefix="/adm")
_service = UsuarioService()


@bp_adm.route("", methods=["POST"])
@jwt_required()
@autorizacao_adm()
def registrar():
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), HTTPStatus.BAD_REQUEST

    try:
        solicitante_id =int(get_jwt_identity())
        _service._exigir_perfil_admin(solicitante_id)

        usuario = _service.cadastrar(
            nome=payload.get("nome"),
            email=payload.get("email"),
            senha=payload.get("senha"),
            perfil=payload.get("perfil"),
            bairro=payload.get("bairro"),
            cidade=payload.get("cidade"),
        )
        return jsonify(usuario.to_dict()), HTTPStatus.CREATED
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro ao registrar usuário: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_adm.route("", methods=["GET"])
@jwt_required()
@autorizacao_adm()
def listar():
    try:
        solicitante_id = int(get_jwt_identity())
        usuarios = _service.listar_todos(solicitante_id=solicitante_id)
        return jsonify([u.to_dict() for u in usuarios]), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro ao listar usuários: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_adm.route("/<int:id>", methods=["GET"])
@jwt_required()
@autorizacao_adm(permitir_proprio=True)
def buscar(id: int):
    try:
        usuario = _service.buscar_por_id(id)
        return jsonify(usuario.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code


@bp_adm.route("/<int:id>", methods=["PUT"])
@jwt_required()
@autorizacao_adm(permitir_proprio=True)
def atualizar(id: int):
    payload = request.get_json(silent=True)
    if not payload:
        return jsonify({"erro": "Corpo da requisição deve ser JSON."}), HTTPStatus.BAD_REQUEST

    try:
        usuario = _service.atualizar(
            usuario_id=id,
            nome=payload.get("nome"),
            email=payload.get("email"),
        )
        return jsonify(usuario.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro ao atualizar usuário: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_adm.route("/filtro-perfil", methods=["GET"])
@jwt_required()
@autorizacao_adm()
def listar_por_perfil():

    perfil_alvo = request.args.get("perfil")
    if not perfil_alvo:
        return jsonify({"erro": "O parâmetro de busca 'perfil' é obrigatório na URL."}), HTTPStatus.BAD_REQUEST

    try:
        solicitante_id = int(get_jwt_identity())
        usuarios = _service.listar_usuarios_por_perfil_adm(
            solicitante_id=solicitante_id,
            perfil_alvo=perfil_alvo
        )
        return jsonify([u.to_dict() for u in usuarios]), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro ao filtrar usuários por perfil: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_adm.route("/<int:id>/status", methods=["PATCH"])
@jwt_required()
@autorizacao_adm()
def alternar_status(id: int):

    payload = request.get_json(silent=True) or {}
    ativo = payload.get("ativo")

    if ativo is None or not isinstance(ativo, bool):
        return jsonify({"erro": "O campo 'ativo' deve ser um valor booleano (true/false)."}), HTTPStatus.BAD_REQUEST

    try:
        solicitante_id = int(get_jwt_identity())
        usuario = _service.alternar_status_usuario_adm(
            solicitante_id=solicitante_id,
            usuario_id=id,
            ativo=ativo
        )
        return jsonify(usuario.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro ao alternar status do usuário: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_adm.route("/<int:id>/perfil", methods=["PATCH"])
@jwt_required()
@autorizacao_adm()
def alterar_perfil(id: int):

    payload = request.get_json(silent=True) or {}
    novo_perfil = payload.get("perfil")

    try:
        solicitante_id = int(get_jwt_identity())
        usuario = _service.alterar_perfil_usuario_adm(
            solicitante_id=solicitante_id,
            usuario_id=id,
            novo_perfil=novo_perfil
        )
        return jsonify(usuario.to_dict()), HTTPStatus.OK
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro ao alterar perfil do usuário: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR


@bp_adm.route("/<int:id>", methods=["DELETE"])
@jwt_required()
@autorizacao_adm()
def deletar(id: int):

    try:
        solicitante_id = int(get_jwt_identity())
        _service.Blacklist_ou_Deletar_usuario_adm(
            solicitante_id=solicitante_id,
            usuario_id=id
        )
        return "", HTTPStatus.NO_CONTENT
    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code
    except Exception as exc:
        logger.error("Erro ao deletar usuário pelo ADM: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor."}), HTTPStatus.INTERNAL_SERVER_ERROR

@bp_adm.route("/me", methods=["DELETE"])
@jwt_required()
def deletar_minha_conta():
    try:
        solicitante_id = int(get_jwt_identity())
        _service.deletar(usuario_id=solicitante_id)
        return "", HTTPStatus.NO_CONTENT

    except AppError as exc:
        return jsonify({"erro": exc.mensagem}), exc.status_code

    except Exception as exc:
        logger.error("Erro ao deletar minha propia conta: %s", exc, exc_info=True)
        return jsonify({"erro": "Erro interno no servidor"}), HTTPStatus.INTERNAL_SERVER_ERROR

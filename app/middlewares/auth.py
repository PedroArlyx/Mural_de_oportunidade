from functools import wraps
from flask import jsonify
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.Exceptions import AppError
from app.services import UsuarioService
import logging


def autorizacao_adm(permitir_proprio=False):
    logger = logging.getLogger(__name__)
    _service = UsuarioService()

    def decorator(f):
        @wraps(f)
        @jwt_required()
        def decorated_function(*args, **Kwargs):
            try:
                solicitante_id = int(get_jwt_identity())
                alvo_id = Kwargs.get("id")

                if permitir_proprio and alvo_id and solicitante_id == alvo_id:
                    return f(*args, **Kwargs)

                _service._exigir_perfil_admin(solicitante_id)

                return f(*args, **Kwargs)
            except AppError as e:
                return jsonify(e.to_dict()), e.status_code
            except Exception as e:
                logger.error("Erro na validacao de seguranca: %s",e, exc_info=True)
                return jsonify({"Error": "Erro interno no servidor"}), HTTPStatus.INTERNAL_SERVER_ERROR
        return decorated_function
    return decorator
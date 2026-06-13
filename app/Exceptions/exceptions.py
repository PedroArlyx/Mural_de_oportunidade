class AppError(Exception):

    status_code: int = 500
    error_type: str = "InternalServerError"

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem

    def to_dict(self):
        return {"status": "error","type": self.error_type, "mensagem": self.mensagem}


class BadRequestError(AppError):
    status_code = 400
    error_type = "BadRequest"


class UnauthorizedError(AppError):
    status_code = 401
    error_type = "Unauthorized"


class ForbiddenError(AppError):
    status_code = 403
    error_type = "Forbidden"


class NotFoundError(AppError):
    status_code = 404
    error_type = "NotFound"


class ConflictError(AppError):
    status_code = 409
    error_type = "Conflict"
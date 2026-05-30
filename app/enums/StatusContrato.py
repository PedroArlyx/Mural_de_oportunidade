from enum import Enum

class StatusContrato(Enum):
    PENDENTE = "pendente"
    ATIVO = "ativo"
    CONCLUIDO = "concluido"
    CANCELADO = "cancelado"
    RESTRITO = "restrito"
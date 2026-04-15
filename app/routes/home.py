from flask import Blueprint

from app.services import AnuncioService

bp_home=Blueprint('main', __name__)

service = AnuncioService()
@bp_home.route('/', methods = ['GET'])
def home():
    return service.listar_anuncios()


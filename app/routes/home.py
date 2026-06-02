from flask import Blueprint,jsonify
from app.services import AnuncioService
from http import HTTPStatus

bp_home=Blueprint('main', __name__)

service = AnuncioService()

@bp_home.route('/', methods = ['GET'])
def home():
    return jsonify({"status":"ok","mensagem":"Mural de Oportunidade Api esta no ar"}), HTTPStatus.OK



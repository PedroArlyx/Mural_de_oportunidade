from flask import Blueprint, render_template
from app.services import AnuncioService

bp_home=Blueprint('main', __name__)

service = AnuncioService()

@bp_home.route('/', methods = ['GET'])
def home():
    anuncios = service.listar()
    return render_template('home.html', anuncios=anuncios)



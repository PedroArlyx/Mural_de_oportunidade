from flask import Blueprint, render_template, redirect
from flask_login import login_required, current_user

from app.services import AnuncioService

bp_home=Blueprint('main', __name__)

service = AnuncioService()

@bp_home.route('/', methods = ['GET'])
def home():
    anuncios = service.listar_anuncios()
    return render_template('index.html', anuncios=anuncios)


@bp_home.route('/admin-painel')
@login_required
def painel_admin():
    if not current_user.admin:
        return redirect('/')

    anuncios = service.listar_anuncios()
    return render_template('index.html', anuncios=anuncios, sou_admin=True)


@bp_home.route('/mural')
@login_required
def mural():
    from app.models import Anuncio

    lista_anuncios = Anuncio.query.order_by(Anuncio.id.desc()).all()

    eh_admin = current_user.admin

    return render_template('index.html',
                           anuncios=lista_anuncios,
                           sou_admin=eh_admin)
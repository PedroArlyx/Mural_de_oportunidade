from flask import Blueprint, render_template, redirect,url_for
from flask_login import login_required, current_user

from app.services import AnuncioService, adminnistrador_service
from app.utils.decorators import admin_required

bp_home=Blueprint('main', __name__)

service = AnuncioService()

@bp_home.route('/')
def hoem():
    return redirect(url_for('login.login'))

@bp_home.route('/admin-painel')
@login_required
@admin_required
def painel_admin():

    anuncios = service.listar_anuncios()
    return render_template('index.html', anuncios=anuncios, sou_admin=True)


@bp_home.route('/mural')
@login_required
def mural():
    lista_anuncios = service.listar_anuncios()

    return render_template('index.html',
                           anuncios=lista_anuncios,
                           sou_admin=current_user.is_admin)
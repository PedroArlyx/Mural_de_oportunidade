
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.services.anuncio_service import AnuncioService

bp_home = Blueprint('main', __name__)
service = AnuncioService()

@bp_home.route('/', methods=['GET'])
def home():
    return service.listar_anuncios()

@bp_home.route('/login_usuario', methods=['POST'])
def login_usuario():
    from app.models.usuario import Usuario
    
    nome = request.form.get('usuario')
    senha = request.form.get('senha')

    usuario_encontrado = Usuario.query.filter_by(nome=nome).first()

    if usuario_encontrado:
        session['usuario_id'] = usuario_encontrado.id
        session['usuario_perfil'] = usuario_encontrado.perfil
        return redirect(url_for('main.home'))
    
    return redirect(url_for('main.home'))

@bp_home.route('/deletar_anuncio/<int:id>')
def deletar_anuncio(id):
    from extensao import bd
    from app.models.anuncio import Anuncio
    
    anuncio = Anuncio.query.get_or_404(id)
    
    if session.get('usuario_perfil') == 'admin':
        bd.session.delete(anuncio)
        bd.session.commit()
        flash('Removido por ADMIN')
    
    return redirect(url_for('main.home'))
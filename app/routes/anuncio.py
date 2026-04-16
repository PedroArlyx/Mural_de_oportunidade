from flask import Blueprint, request, redirect, flash, url_for
from app.services import AnuncioService
from flask_login import current_user, login_required

bp_anuncio = Blueprint('anuncio', __name__,url_prefix='/anuncio')

service = AnuncioService()

@bp_anuncio.route('/criar', methods=['GET','POST'])
@login_required
def criar_anuncio():

    if request.method == 'POST':

        prestador_id = current_user.id
        categoria_id = request.form.get('categoria_id')
        titulo = request.form.get('titulo')
        descricao = request.form.get('descricao')
        preco = request.form.get('preco')

        if not titulo or not descricao or not preco or not categoria_id:
            return "preencha todos os campos obrigatorios"

        try:
            preco = float(preco)
        except ValueError:
            return "Precisa ser um valor numerico"

        resultado=service.criar_anuncio(prestador_id,
                categoria_id,
                titulo,
                descricao,
                preco)

        return str(resultado)

@bp_anuncio.route('/deletar/<int:id>',methods = ['POST'])
@login_required
def deletar_anuncio(id):

    usuario_id = current_user.id

    resultado = service.deletar_anuncio(id,current_user.id,current_user.is_admin)
    flash(resultado)

    return redirect(url_for('main.mural'))

@bp_anuncio.route('/atualizar/<int:id>',methods = ['POST'])
@login_required
def atualizar_anuncio(id):

    usuario_id = current_user.id
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco')

    if not titulo or not descricao or not preco:
        return "Preencha todos os campos obrigatorios"

    try:
        preco = float(preco)
    except ValueError:
        return "Preco invalido"

    anuncio = service.atualizar_anuncio(id,usuario_id,titulo,descricao,preco)

    return "anucio atualizado"



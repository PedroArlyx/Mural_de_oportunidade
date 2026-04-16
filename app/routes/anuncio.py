from flask import Blueprint, request, redirect, url_for, flash
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

        if not titulo or not descricao or not preco :
            flash("Preencha todos os campos!", "error")
            return redirect(url_for('main.home'))


        try:
            preco = float(preco)
        except ValueError:
            return "Precisa ser um valor numerico"

        anuncio=service.criar_anuncio(prestador_id,
                categoria_id,
                titulo,
                descricao,
                preco)

        return redirect(url_for('main.home'))

@bp_anuncio.route('/deletar/<int:id>',methods = ['POST'])
@login_required
def deletar_anuncio(id):

    usuario_id = current_user.id

    resultado = service.deletar_anuncio(id,usuario_id)

    return redirect(url_for('main.home'))

@bp_anuncio.route('/atualizar/<int:id>',methods = ['POST'])
@login_required
def atualizar_anuncio(id):

    usuario_id = current_user.id
    titulo = request.form.get('titulo')
    descricao = request.form.get('descricao')
    preco = request.form.get('preco')

    if not titulo or not descricao or not preco:
        flash("Preencha todos os campos!", "error")
        return redirect(url_for('main.home'))

    try:
        preco = float(preco)
    except ValueError:
        return "Preco invalido"

    anuncio = service.atualizar_anuncio(id,usuario_id,titulo,descricao,preco)

    return redirect(url_for('main.home'))

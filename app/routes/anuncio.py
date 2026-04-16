from flask import Blueprint, request, redirect, flash, url_for


from app.models import Anuncio
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

        anuncio=service.criar_anuncio(prestador_id,
                categoria_id,
                titulo,
                descricao,
                preco)

        return "anuncio criado"

@bp_anuncio.route('/deletar/<int:id>',methods = ['POST'])
@login_required
def deletar_anuncio(id):

    usuario_id = current_user.id

    resultado = service.deletar_anuncio(id,usuario_id)

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


@bp_anuncio.route('/cadastrar', methods=['POST'])
@login_required
def cadastrar():
    from extensao import bd as db
    from app.models import Anuncio

    novo_anuncio = Anuncio(
        titulo=request.form.get('titulo'),
        descricao=request.form.get('descricao'),
        preco=float(request.form.get('preco').replace(',', '.')) if request.form.get('preco') else 0.0,
        categoria_id=int(request.form.get('categoria')) if request.form.get('categoria') else 1,
        prestador_id=current_user.id
    )

    db.session.add(novo_anuncio)
    db.session.commit()

    return redirect(url_for('main.mural'))
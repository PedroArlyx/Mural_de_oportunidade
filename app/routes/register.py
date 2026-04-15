from flask import Blueprint, render_template, request, redirect
from app.services import UsuarioService

bp_register = Blueprint('register',__name__,url_prefix='/register')

service = UsuarioService()

@bp_register.route('/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        perfil = request.form.get('perfil')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')

        if not nome or not email or not senha:
            return "Preencha todos os campos"

        usuario =service.cadastrarUsuario(nome,email,senha,perfil,bairro,cidade)

        if not usuario:
            return"Email ja cadastrado"

        return "Usuário cadastrado com sucesso!"
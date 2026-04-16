from flask import Blueprint, render_template, request, redirect, url_for
from app.services import UsuarioService,AdministradorService

bp_register = Blueprint('register',__name__,url_prefix='/register')

service = UsuarioService()
adm_service = AdministradorService()

@bp_register.route('/', methods=['GET','POST'])
def register_usuario():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        perfil = request.form.get('perfil')
        bairro = request.form.get('bairro')
        cidade = request.form.get('cidade')

        if not nome or not email or not senha:
            return "Preencha todos os campos"

        usuario =service.cadastrar_usuario(nome,email,senha,perfil,bairro,cidade)

        if not usuario:
            return"Email ja cadastrado"

    return redirect(url_for('login.login'))

@bp_register.route('/adm', methods=['GET','POST'])
def register_admin():
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

        if not resultado:
            return"Email ja cadastrado"

        if isinstance(resultado , str):
            return resultado

    return redirect(url_for('login.login'))
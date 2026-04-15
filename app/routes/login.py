from flask import Blueprint,render_template,request,redirect
from app.services import UsuarioService
from flask_login import login_user,logout_user,login_required, current_user

bp_login = Blueprint('login', __name__, url_prefix='/login')

service=UsuarioService()

@bp_login.route('/',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/home')

    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')

        usuario = service.login(email,senha)
        if not usuario:
            return "Email ou senha incorretos"

        login_user(usuario)

        return "usuario logado com sucesso!"

@bp_login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect ('/login')
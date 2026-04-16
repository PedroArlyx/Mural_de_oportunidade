from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app.models import Usuario
from app.services import UsuarioService
from flask_login import login_user,logout_user,login_required, current_user

from app.services import AdministradorService

bp_login = Blueprint('login', __name__, url_prefix='/login')

service_usuario = UsuarioService()
service_admin = AdministradorService()

@bp_login.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.mural'))

    if request.method == 'POST':
        email = request.form.get('email').strip()
        senha = request.form.get('senha')


        usuario = service_usuario.login(email, senha)

        if not isinstance(usuario,str) and usuario:
            login_user(usuario)
            return redirect(url_for(''))
        admin = service_admin.login_admin(email, senha)

        if not isinstance(admin,str)  and admin:
            login_user(admin)
            return redirect(url_for(''))

        flash("Email ou senha incorretos")
        return redirect(url_for(''))

    return render_template('login.html')

@bp_login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect ('/login')



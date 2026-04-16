from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app.models import Usuario
from app.services import UsuarioService
from flask_login import login_user,logout_user,login_required, current_user

bp_login = Blueprint('login', __name__, url_prefix='/login')

service=UsuarioService()

@bp_login.route('/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.mural'))

    if request.method == 'POST':
        email = request.form.get('email').strip()
        senha = request.form.get('senha')
        origem = request.form.get('origem')

        usuario = Usuario.query.filter(Usuario.email.ilike(email)).first()

        if not usuario or not check_password_hash(usuario.senha_hash, senha):
            flash("E-mail ou senha incorretos!", "danger")
            return redirect(url_for('login.login'))

        if origem == 'admin':
            if usuario.admin:
                login_user(usuario)
                return redirect(url_for('main.painel_admin'))
            else:
                flash("Acesso negado: você não é um administrador", "danger")
                return redirect(url_for('login.login'))
        elif origem == 'usuario':
            login_user(usuario)
            return redirect(url_for('main.home'))

    return render_template('login.html')

@bp_login.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect (url_for('login.login'))



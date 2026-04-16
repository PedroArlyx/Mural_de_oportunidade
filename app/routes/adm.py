from flask import Blueprint, render_template, redirect, url_for , flash
from flask_login import login_required, current_user
from app.services import Adm_Service
from app.utils.decorators import admin_required

bp_adm = Blueprint('adm', __name__, url_prefix='/adm')

service = Adm_Service()

@bp_adm.route('/usuarios')
@login_required
@admin_required
def listar_Usuarios():
    usuario = service.listar_todos_usuarios()
    return render_template('')

@bp_adm.route('/usuario/<int:id>', methods = ['GET','POST'])
@login_required
@admin_required
def deletar_Usuario(id):
    service.deletar_usuario(id, current_user.is_admin)
    return redirect('/adm/usuarios')
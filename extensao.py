from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


login_manager = LoginManager()
bd = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    from app.models import Administrador,Usuario

    try:
        tipo, id_numerico = user_id.split('_')
        id_numerico = int(id_numerico)

        if tipo =='adm':
            return bd.sessin.get(Administrador,id_numerico)
        elif tipo == 'user':
            return bd.session.get(Usuario,id_numerico)
    except:
        return None
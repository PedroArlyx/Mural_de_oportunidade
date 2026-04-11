from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

#instanciar objetos ao login manager
login_manager = LoginManager()
bd = SQLAlchemy()
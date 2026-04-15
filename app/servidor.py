from flask import Flask
from extensao import bd
from app.routes import bp_home,bp_login,bp_register,bp_anuncio
from extensao import login_manager

def create_app():

     app = Flask(__name__)
     app.config['SECRET_KEY'] = '12734464exdf'

     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg://postgres:12345@localhost:5432/monkey'
     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
     app.config['SQLALCHEMY_ECHO'] = True


     bd.init_app(app)
     login_manager.init_app(app)
     login_manager.login_view = 'login.login'

     app.register_blueprint(bp_home)
     app.register_blueprint(bp_login)
     app.register_blueprint(bp_register)
     app.register_blueprint(bp_anuncio)

     return app
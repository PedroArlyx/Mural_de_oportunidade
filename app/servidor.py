from flask import Flask
from app.extensao import bd
from app.routes import bp_home,bp_anuncios,bp_adm, auth_bp,bp_contratos,bp_categorias,bp_avaliacao
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
import os
from flask_cors import CORS

load_dotenv()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = False

    bd.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(bp_categorias)
    app.register_blueprint(bp_contratos)
    app.register_blueprint(bp_home)
    app.register_blueprint(bp_anuncios)
    app.register_blueprint(bp_adm)
    app.register_blueprint(bp_avaliacao)

    return app

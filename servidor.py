#no terminal => pip install flask
from flask import *
from blueprints.bp_professor import  bp_prof
from extensao import bd
from extensao import login_manager

def criar_servidor():
    #instanciando o servidor web flask
    app = Flask(__name__)
    #gerar chave secreta para ser usado no controle de ssão(cookies)
    app.config['SECRET KEY'] = '1234567890'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:AdminHenri21@localhost:5432/infoweb20261'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    bd.init_app(app)

    #vinculando o login mananger ao servidor flask
    login_manager.init_app(app)
    login_manager.login_view = 'home_page'

    #vinculando cada blueprint com o servidor flask
    app.register_blueprint(bp_prof)


    #criando uma rota (endpoint) de acesso no backend
    @app.route('/')
    def home_page():
        return render_template("login.html")

    #retornando objerto que representa o servido flask craido
    return app

if __name__ == '__main__':
    app = criar_servidor()
    with app.app_context():
        bd.create_all()
    app.run(debug=True)
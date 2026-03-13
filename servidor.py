#no terminal => pip install flask
from flask import *
from blueprints.bp_professor import  bp_prof
from extensao import bd


def criar_servidor():
    #instanciando o servidor web flask
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:12345@localhost:5432/infoweb20261'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['SQLALCHEMY_ECHO'] = True
    bd.init_app(app)

    #vinculando cada blueprint com o servidor flask
    app.register_blueprint(bp_prof)


    #criando uma rota (endpoint) de acesso no backend
    @app.route('/')
    def home_page():
        return render_template("login.html")


    return app


if __name__ == '__main__':
    app = criar_servidor()
    with app.app_context():
        bd.create_all()
    app.run(debug=True)


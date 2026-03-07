#no terminal => pip install flask
from flask import *
from blueprints.bp_professor import  bp_prof

def criar_servidor():
    #instanciando o servidor web flask
    app = Flask(__name__)

    #vinculando cada blueprint com o servidor flask
    app.register_blueprint(bp_prof)


    #criando uma rota (endpoint) de acesso no backend
    @app.route('/')
    def home_page():
        return render_template("login.html")


    return app


if __name__ == '__main__':
    app = criar_servidor()
    app.run()


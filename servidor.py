from flask import *


def criar_servidor():
    #instanciando o servidor web flask
    app = Flask(__name__)

    #criando uma rota (endpoint) de acesso no backend
    @app.route('/')
    def home_page():

        return 'minha primeira pagina uhuuuuu'

    return app


if __name__ == '__main__':
    app = criar_servidor()
    app.run()


from app.servidor import create_app
from extensao import bd
from app.models import usuario,anuncio,categoria

if __name__ == '__main__':
    servidor=create_app()
    with servidor.app_context():
        bd.create_all()
    servidor.run(debug=True)
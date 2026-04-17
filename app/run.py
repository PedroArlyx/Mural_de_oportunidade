from app.servidor import create_app
from app.extensao import bd

if __name__ == '__main__':
    servidor=create_app()
    with servidor.app_context():
        bd.create_all()
    servidor.run(debug=True)
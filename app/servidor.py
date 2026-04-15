from flask import Flask
from extensao import db  # Importa o db que você criou

def create_app():
    app = Flask(__name__)
    
    # 1. Configuração do seu Banco de Dados (Postgres)
    # Substitua 'usuario', 'senha' e 'nome_do_banco' pelos seus dados
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:suasenha@localhost:5432/projeto_mural'
    app.config['SECRET_KEY'] = 'uma_chave_bem_segura'

    # 2. Conecta o db ao aplicativo Flask
    db.init_app(app)

    # 3. Registra as suas rotas
    from app.routes.home import bp as home_bp
    app.register_blueprint(home_bp)

    return app
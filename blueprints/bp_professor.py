from flask import Blueprint, request, render_template

from dao.professor_dao import ProfessorDao

#faz login, lista alunos, adiciona aluno, remove aluno

professor_dao = ProfessorDao()


#instanciei uma blueprint para que eu possa usar para criar rotas
bp_prof = Blueprint('professor', __name__, url_prefix='/professor')

@bp_prof.route('/login', methods=['POST'])
def fazer_login_professor():
    login = request.form.get('usuario')
    senha = request.form.get('senha')

    professor_dao.verificar_login(login, senha)

    return 'deu certo'

@bp_prof.route('/cadastrar', methods=['POST', 'GET'])
def cadastrar_professor():
    if request.method == 'GET':
        return render_template('cadastrarprofessor.html')

    nome = request.form.get('nome')
    email = request.form.get('email')
    senha = request.form.get('senha')
    nome_projeto = request.form.get('nome_projeto')

    #chama o dao para que seja inserido no banco de dados
    saida = professor_dao.cadastrar_professor(nome, email, senha, nome_projeto)
    if saida:
        return render_template('login.html')
    else:
        return render_template('login.html')#falta adicionar mensagem de erro






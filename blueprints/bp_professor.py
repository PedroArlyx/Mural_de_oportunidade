from flask import Blueprint, request

#faz login, lista alunos, adiciona aluno, remove aluno

#instanciei uma blueprint para que eu possa usar para criar rotas
bp_prof = Blueprint('professor', __name__, url_prefix='/professor')

@bp_prof.route('/login', methods=['POST'])
def fazer_login_professor():
    login = request.form.get('usuario')
    senha = request.form.get('senha')

    return 'deu certo'


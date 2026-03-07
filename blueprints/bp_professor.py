from flask import Blueprint

#faz login, lista alunos, adiciona aluno, remove aluno

#instanciei uma blueprint para que eu possa usar para criar rotas
bp_prof = Blueprint('professor', __name__, url_prefix='/professor')

@bp_prof.route('/oi')
def teste():
    return 'fala ai doidao'


@bp_prof.route('/')
def teste2():
    return 'KKKKKKKKKKKK'
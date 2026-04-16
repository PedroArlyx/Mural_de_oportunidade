from app.models.anuncio import Anuncio
from app.repositories import AnuncioRepo


class AnuncioService:
    def __init__(self):
        self.anuncio_Repo = AnuncioRepo()

    def criar_anuncio(self,prestador_id, categoria_id,titulo,descricao,preco):
        if preco < 0:
            return "Preco nao poder ser negativo"

        anuncio = Anuncio(prestador_id=prestador_id,categoria_id=categoria_id,titulo = titulo,descricao= descricao,preco=preco,status='ativo')
        return self.anuncio_Repo.salvar_anuncio(anuncio)

    def listar_anuncios(self):
        return self.anuncio_Repo.listar_todos_anuncios()

    def atualizar_anuncio(self,id,usuario_id,titulo,descricao,preco):
        anuncio = self.anuncio_Repo.buscar_por_id(id)

        if not anuncio:
           return "Anuncio nao encontrado"

        if anuncio.prestador_id != usuario_id:
            return "vc nao tem permissao para aditar esse anuncio"

        if preco < 0:
            return "Preco nao poder ser negativo"

        if not titulo or not descricao:
            return "Dados invalidos"

        anuncio.titulo = titulo
        anuncio.descricao = descricao
        anuncio.preco = preco

        return self.anuncio_Repo.salvar_anuncio(anuncio)

    def deletar_anuncio(self,id,usuario_id,is_admin = False):
        anuncio = self.anuncio_Repo.buscar_por_id(id)

        if not anuncio:
            return "anuncio nao encotrado"

        if anuncio.prestador_id != usuario_id and not is_admin:
            return "voce nao tem permissao para deletar esse anuncio"

        self.anuncio_Repo.deletar_anuncio(anuncio)

        return "anuncio deletado"




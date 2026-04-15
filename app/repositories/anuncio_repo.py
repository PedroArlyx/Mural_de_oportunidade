from extensao import bd
from app.models import Anuncio

class AnuncioRepo:

    def salvar_anuncio(self, anuncio):
        bd.session.add(anuncio)
        bd.session.commit()
        return anuncio
    def listar_todos_anuncios(self):
        return Anuncio.query.all()
        return str(Anuncio)
    def deletar_anuncio(self, anuncio):
        bd.session.delete(anuncio)
        bd.session.commit()
    def atualizar_anuncio(self, anuncio):
        bd.session.add(anuncio)
        bd.session.commit()

    def buscar_por_id(self,id ):
        return Anuncio.query.get(id)
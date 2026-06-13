from app.extensao import bd
from app.models import Anuncio
from typing import List, Optional


class AnuncioRepo:

    def salvar_anuncio(self, anuncio: Anuncio)-> Anuncio:
        try:
            bd.session.add(anuncio)
            bd.session.commit()
            return anuncio
        except Exception :
            bd.session.rollback()
            raise

    def listar_todos_anuncios(self) -> List[Anuncio]:
        return Anuncio.query.all()

    def deletar_anuncio(self, anuncio: Anuncio) -> None:
        try:
            bd.session.delete(anuncio)
            bd.session.commit()
        except Exception :
            bd.session.rollback()
            raise

    def atualizar_anuncio(self, anuncio: Anuncio) -> Anuncio:
        try:
            bd.session.add(anuncio)
            bd.session.commit()
            return anuncio
        except Exception :
            bd.session.rollback()
            raise

    def buscar_por_id(self, id: int) -> Optional[Anuncio]:
        return Anuncio.query.get(Anuncio,id)

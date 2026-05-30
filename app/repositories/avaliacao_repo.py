from app.models import Anuncio,Avaliacao
from app.extensao import bd


class AvaliacaoRepo:

    def avaliar_anuncio(self, avaliacao:  Avaliacao) -> Avaliacao:
        try:
            bd.session.add(avaliacao)
            bd.session.commit()
            return avaliacao
        except Exception  :
            bd.session.rollback()
            raise

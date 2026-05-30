from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
from app.extensao import bd
from app.models.categoria import Categoria


class RepositoryError(Exception):

    def __init__(self, mensagem: str):
        self.mensagem = mensagem
        super().__init__(self.mensagem)


class CategoriaRepo:
    def criar(self, nome: str) -> Categoria:
        try:
            nova_categoria = Categoria(nome=nome.strip())
            bd.session.add(nova_categoria)
            bd.session.commit()
            return nova_categoria
        except SQLAlchemyError as exc:
            bd.session.rollback()
            raise RepositoryError(f"Erro ao salvar a categoria '{nome}': {str(exc)}")

    def buscar_por_id(self, categoria_id: int) -> Optional[Categoria]:
        try:
            return bd.session.get(Categoria, categoria_id)
        except SQLAlchemyError as exc:
            raise RepositoryError(f"Erro ao buscar categoria com ID {categoria_id}: {str(exc)}")

    def buscar_por_nome(self, nome: str) -> Optional[Categoria]:
        try:
            return bd.session.query(Categoria).filter(Categoria.nome.ilike(nome.strip())).first()
        except SQLAlchemyError as exc:
            raise RepositoryError(f"Erro ao buscar categoria com nome '{nome}': {str(exc)}")

    def listar_todas(self) -> List[Categoria]:
        try:
            return bd.session.query(Categoria).all()
        except SQLAlchemyError as exc:
            raise RepositoryError(f"Erro ao listar categorias: {str(exc)}")

    def atualizar(self, categoria_id: int, novo_nome: str) -> Optional[Categoria]:
        try:
            categoria = bd.session.get(Categoria, categoria_id)
            if categoria:
                categoria.nome = novo_nome.strip()
                bd.session.commit()
                return categoria
            return None
        except SQLAlchemyError as exc:
            bd.session.rollback()
            raise RepositoryError(f"Erro ao atualizar a categoria ID {categoria_id}: {str(exc)}")

    def deletar(self, categoria_id: int) -> bool:
        try:
            categoria = bd.session.get(Categoria, categoria_id)
            if categoria:
                bd.session.delete(categoria)
                bd.session.commit()
                return True
            return False
        except SQLAlchemyError as exc:
            bd.session.rollback()
            raise RepositoryError(f"Erro ao deletar a categoria ID {categoria_id}: {str(exc)}")
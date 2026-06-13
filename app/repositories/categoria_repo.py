from typing import List, Optional
from app.extensao import bd
from app.models import Categoria

class CategoriaRepo:
    def criar(self, nome: str) -> Categoria:
        try:
            nova_categoria = Categoria(nome=nome.strip())
            bd.session.add(nova_categoria)
            bd.session.commit()
            return nova_categoria
        except Exception as exc:
            bd.session.rollback()
            raise Exception(f"Erro ao salvar a categoria '{nome}': {str(exc)}")

    def buscar_por_id(self, categoria_id: int) -> Optional[Categoria]:
        try:
            return bd.session.get(Categoria, categoria_id)
        except Exception as exc:
            raise Exception(f"Erro ao buscar categoria com ID {categoria_id}: {str(exc)}")

    def buscar_por_nome(self, nome: str) -> Optional[Categoria]:
        try:
            return bd.session.query(Categoria).filter(Categoria.nome.ilike(nome.strip())).first()
        except Exception as exc:
            raise Exception(f"Erro ao buscar categoria com nome '{nome}': {str(exc)}")

    def listar_todas(self) -> List[Categoria]:
        try:
            return bd.session.query(Categoria).all()
        except Exception as exc:
            raise Exception(f"Erro ao listar categorias: {str(exc)}")

    def atualizar(self, categoria_id: int, novo_nome: str) -> Optional[Categoria]:
        try:
            categoria = bd.session.get(Categoria, categoria_id)
            if categoria:
                categoria.nome = novo_nome.strip()
                bd.session.commit()
                return categoria
            return None
        except Exception as exc:
            bd.session.rollback()
            raise Exception(f"Erro ao atualizar a categoria ID {categoria_id}: {str(exc)}")

    def deletar(self, categoria_id: int) -> bool:
        try:
            categoria = bd.session.get(Categoria, categoria_id)
            if categoria:
                bd.session.delete(categoria)
                bd.session.commit()
                return True
            return False
        except Exception as exc:
            bd.session.rollback()
            raise Exception(f"Erro ao deletar a categoria ID {categoria_id}: {str(exc)}")
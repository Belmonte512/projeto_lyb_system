from src.config import Session
from src.models.entities import Livro

class LivroController:
    def criar_livro(self, titulo, autor, isbn, ano):
        """Insere um novo livro no banco"""
        session = Session()
        try:
            # Validação básica
            if not titulo or not autor:
                return False, "Título e Autor são obrigatórios."
            
            novo_livro = Livro(
                titulo=titulo,
                autor=autor,
                isbn=isbn,
                ano_publicacao=int(ano) if ano else None,
                disponivel=True
            )
            session.add(novo_livro)
            session.commit()
            return True, "Livro cadastrado com sucesso!"
        except Exception as e:
            session.rollback()
            return False, f"Erro ao salvar: {str(e)}"
        finally:
            session.close()

    def listar_livros(self):
        """Retorna todos os livros cadastrados"""
        session = Session()
        try:
            livros = session.query(Livro).all()
            # Precisamos desanexar os objetos da sessão para usar na UI após o close()
            # Ou retornamos uma lista de dicionários (mais seguro para UI)
            dados = []
            for l in livros:
                dados.append({
                    'id': l.id,
                    'titulo': l.titulo,
                    'autor': l.autor,
                    'isbn': l.isbn,
                    'ano': l.ano_publicacao,
                    'status': 'Disponível' if l.disponivel else 'Emprestado'
                })
            return dados
        except Exception as e:
            print(e)
            return []
        finally:
            session.close()

    def excluir_livro(self, livro_id):
        """Remove um livro pelo ID"""
        session = Session()
        try:
            livro = session.query(Livro).filter(Livro.id == livro_id).first()
            if livro:
                session.delete(livro)
                session.commit()
                return True, "Livro removido."
            return False, "Livro não encontrado."
        except Exception as e:
            return False, f"Erro ao excluir: {e}"
        finally:
            session.close()
from src.config import Session
from src.models.entities import Emprestimo, Livro, Aluno
from datetime import datetime

class EmprestimoController:
    def realizar_emprestimo(self, aluno_matricula, livro_isbn):
        """Processa a retirada de um livro."""
        session = Session()
        try:
            # 1. VALIDAÇÃO DO LIVRO
            livro = session.query(Livro).filter(Livro.isbn == livro_isbn).first()
            if not livro:
                return False, "Livro (ISBN) não encontrado."
            if not livro.disponivel:
                return False, f"O livro '{livro.titulo}' já está emprestado."

            # 2. VALIDAÇÃO DO ALUNO
            aluno = session.query(Aluno).filter(Aluno.matricula == aluno_matricula).first()
            if not aluno:
                return False, "Aluno (Matrícula) não encontrado."

            # 3. CRIAÇÃO DA TRANSAÇÃO
            novo_emprestimo = Emprestimo(
                livro_id=livro.id,
                aluno_id=aluno.id,
                data_retirada=datetime.now(),
                status="Ativo"
            )
            session.add(novo_emprestimo)

            # 4. ATUALIZAÇÃO DO STATUS DO LIVRO (CRÍTICO)
            livro.disponivel = False
            
            session.commit()
            return True, f"Empréstimo realizado. Livro: {livro.titulo} para {aluno.nome}."
        except Exception as e:
            session.rollback()
            return False, f"Erro ao realizar empréstimo: {str(e)}"
        finally:
            session.close()

    def realizar_devolucao(self, emprestimo_id):
        """Processa a devolução de um livro."""
        session = Session()
        try:
            emprestimo = session.query(Emprestimo).filter(Emprestimo.id == emprestimo_id).first()
            
            if not emprestimo:
                return False, "Empréstimo não encontrado."
            if emprestimo.data_devolucao is not None:
                return False, "Este livro já foi devolvido."

            # 1. ATUALIZAÇÃO DO STATUS DO EMPRÉSTIMO
            emprestimo.data_devolucao = datetime.now()
            emprestimo.status = "Finalizado"

            # 2. ATUALIZAÇÃO DO STATUS DO LIVRO (CRÍTICO)
            livro = session.query(Livro).filter(Livro.id == emprestimo.livro_id).first()
            if livro:
                livro.disponivel = True
            
            session.commit()
            return True, f"Devolução registrada com sucesso. Livro: {livro.titulo}."
        except Exception as e:
            session.rollback()
            return False, f"Erro ao registrar devolução: {str(e)}"
        finally:
            session.close()

    def listar_emprestimos(self, status="Ativo"):
        """Lista todos os empréstimos (Ativos ou Histórico)."""
        session = Session()
        try:
            query = session.query(Emprestimo).filter(Emprestimo.status == status).all()
            
            dados = []
            for e in query:
                # Carrega o nome do Aluno e o Título do Livro para a visualização
                aluno = session.query(Aluno).filter(Aluno.id == e.aluno_id).first()
                livro = session.query(Livro).filter(Livro.id == e.livro_id).first()

                dados.append({
                    'id': e.id,
                    'livro_titulo': livro.titulo if livro else "N/A",
                    'aluno_nome': aluno.nome if aluno else "N/A",
                    'data_retirada': e.data_retirada.strftime('%Y-%m-%d'),
                    'data_devolucao': e.data_devolucao.strftime('%Y-%m-%d') if e.data_devolucao else 'Pendente',
                    'status': e.status
                })
            return dados
        except Exception as e:
            print(f"Erro ao listar empréstimos: {e}")
            return []
        finally:
            session.close()
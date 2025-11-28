from src.config import Session
from src.models.entities import Aluno # Importe a entidade Aluno
from src.models.entities import Aluno, Emprestimo # <--- ADICIONE Emprestimo

class AlunoController:
    def criar_aluno(self, nome, matricula, email):
        """Insere um novo aluno no banco de dados."""
        session = Session()
        try:
            if not nome or not matricula:
                return False, "Nome e Matrícula são obrigatórios."
            
            # Verificar se a matrícula já existe
            aluno_existente = session.query(Aluno).filter(Aluno.matricula == matricula).first()
            if aluno_existente:
                return False, "Matrícula já cadastrada no sistema."

            novo_aluno = Aluno(
                nome=nome,
                matricula=matricula,
                curso="",  # Curso pode ser opcional ou vazio
                email=email,
            )
            session.add(novo_aluno)
            session.commit()
            return True, f"Aluno {nome} cadastrado com sucesso!"
        except Exception as e:
            session.rollback()
            return False, f"Erro ao salvar aluno: {str(e)}"
        finally:
            session.close()

    def listar_alunos(self):
        """Retorna todos os alunos cadastrados."""
        session = Session()
        try:
            alunos = session.query(Aluno).all()
            dados = []
            for a in alunos:
                dados.append({
                    'id': a.id,
                    'nome': a.nome,
                    'matricula': a.matricula,
                    'email': a.email,
                    'emprestimos': 0
                })
            return dados
        except Exception as e:
            print(e)
            return []
        finally:
            session.close()
            
    def buscar_aluno_por_id(self, aluno_id):
        """Busca um aluno pelo ID primário."""
        session = Session()
        try:
            return session.query(Aluno).filter(Aluno.id == aluno_id).first()
        finally:
            session.close()

    def excluir_aluno(self, aluno_id):
        """Remove um aluno pelo ID, verificando empréstimos ativos."""
        session = Session()
        try:
            aluno = session.query(Aluno).filter(Aluno.id == aluno_id).first()
            if not aluno:
                return False, "Aluno não encontrado."

            # CORREÇÃO: Faz a contagem dos empréstimos ativos via consulta
            emprestimos_ativos_count = session.query(Emprestimo).filter(
                Emprestimo.aluno_id == aluno_id,
                Emprestimo.data_devolucao.is_(None) # Empréstimos sem data de devolução são ativos
            ).count()
            
            if emprestimos_ativos_count > 0:
                return False, f"O aluno tem {emprestimos_ativos_count} empréstimo(s) ativo(s) e não pode ser excluído."
                
            session.delete(aluno)
            session.commit()
            return True, "Aluno removido com sucesso."
        except Exception as e:
            session.rollback()
            return False, f"Erro ao excluir: {e}"
        finally:
            session.close()
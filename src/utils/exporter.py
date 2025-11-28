import json
import zipfile
import os
from datetime import datetime
from src.config import Session, BASE_DIR
from src.models.entities import Livro, Aluno, Emprestimo

class DataExporter:
    def exportar_dados(self):
        """
        1. Lê todas as tabelas.
        2. Gera um JSON único.
        3. Cria um arquivo ZIP contendo esse JSON.
        Retorna: (Sucesso: bool, Mensagem: str)
        """
        session = Session()
        try:
            # 1. Coleta de Dados
            livros = session.query(Livro).all()
            alunos = session.query(Aluno).all()
            emprestimos = session.query(Emprestimo).all()

            # 2. Serialização (Converter Objetos -> Dicts)
            data = {
                "metadata": {
                    "data_exportacao": str(datetime.now()),
                    "versao_sistema": "1.0"
                },
                "livros": [
                    {
                        "id": l.id,
                        "titulo": l.titulo,
                        "autor": l.autor,
                        "isbn": l.isbn,
                        "ano": l.ano_publicacao,
                        "disponivel": l.disponivel
                    } for l in livros
                ],
                "alunos": [
                    {
                        "id": a.id,
                        "nome": a.nome,
                        "matricula": a.matricula,
                        "curso": a.curso,
                        "email": a.email
                    } for a in alunos
                ],
                "emprestimos": [
                    {
                        "id": e.id,
                        "livro_id": e.livro_id,
                        "aluno_id": e.aluno_id,
                        "data_retirada": str(e.data_retirada),
                        "data_devolucao": str(e.data_devolucao) if e.data_devolucao else None,
                        "status": e.status
                    } for e in emprestimos
                ]
            }

            # 3. Definição de Caminhos
            # Salvaremos na pasta 'data/' do projeto
            output_dir = os.path.join(BASE_DIR, 'data')
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            json_filename = "biblioteca_backup.json"
            zip_filename = "backup_sistema.zip"
            
            json_path = os.path.join(output_dir, json_filename)
            zip_path = os.path.join(output_dir, zip_filename)

            # 4. Escrita do JSON
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            # 5. Criação do ZIP
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                zipf.write(json_path, arcname=json_filename)
                
            # Limpeza: Remove o JSON cru, deixando apenas o ZIP (opcional, mas mais limpo)
            os.remove(json_path)

            return True, f"Exportação concluída com sucesso!\nArquivo salvo em:\n{zip_path}"

        except Exception as e:
            return False, f"Erro na exportação: {str(e)}"
        finally:
            session.close()
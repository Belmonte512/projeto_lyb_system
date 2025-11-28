import requests
import json
from datetime import datetime
from src.config import Session
from src.models.entities import DadosImportados

class WebImporter:
    def __init__(self):
        # API Pública para teste (Simula um sistema externo de RH ou parceiros)
        self.url_origem = "https://jsonplaceholder.typicode.com/users"

    def importar_dados_externos(self):
        """
        1. Faz GET na URL.
        2. Salva o JSON bruto no banco para histórico.
        3. Retorna os dados parseados para a UI mostrar.
        """
        session = Session()
        try:
            # 1. Requisição Web
            response = requests.get(self.url_origem, timeout=10)
            response.raise_for_status() # Garante que não houve erro 404/500
            
            dados_lista = response.json()
            
            # 2. Serialização para salvar no Banco (Armazenamento Persistente)
            json_string = json.dumps(dados_lista, ensure_ascii=False)
            
            novo_import = DadosImportados(
                origem_url=self.url_origem,
                conteudo_json=json_string,
                data_importacao=datetime.now()
            )
            session.add(novo_import)
            session.commit()
            
            return True, dados_lista, "Dados importados e arquivados com sucesso!"
            
        except requests.exceptions.RequestException as e:
            return False, [], f"Erro de Conexão: {e}"
        except Exception as e:
            session.rollback()
            return False, [], f"Erro interno: {e}"
        finally:
            session.close()

    def recuperar_ultimo_import(self):
        """Busca o último JSON salvo no banco para exibir na tela (Persistência)."""
        session = Session()
        try:
            registro = session.query(DadosImportados).order_by(DadosImportados.id.desc()).first()
            if registro:
                return json.loads(registro.conteudo_json), registro.data_importacao
            return [], None
        finally:
            session.close()
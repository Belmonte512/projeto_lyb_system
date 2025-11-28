from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Caminho absoluto para garantir que o banco seja criado na pasta 'data'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'data', 'library.db')
CONN_STRING = f'sqlite:///{DB_PATH}'

# Engine global
engine = create_engine(CONN_STRING, echo=False) # echo=True para ver o SQL no console
Session = sessionmaker(bind=engine)

def init_db():
    """Cria as tabelas se não existirem"""
    from src.models.entities import Base
    
    # Garante que a pasta data existe
    if not os.path.exists(os.path.join(BASE_DIR, 'data')):
        os.makedirs(os.path.join(BASE_DIR, 'data'))
        
    Base.metadata.create_all(engine)
    print(f"Banco de dados inicializado em: {DB_PATH}")
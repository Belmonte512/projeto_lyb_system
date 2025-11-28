from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

# Criação da Base Declarativa
Base = declarative_base()

class Usuario(Base):
    """Tabela de Usuários do Sistema (Bibliotecários)"""
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    senha_hash = Column(String(200), nullable=False) # Armazenaremos hash, nunca texto plano
    nome_completo = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f"<Usuario(nome='{self.username}')>"

class Livro(Base):
    """Tabela de Acervo"""
    __tablename__ = 'livros'

    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    autor = Column(String(100), nullable=False)
    isbn = Column(String(20), unique=True, nullable=True)
    ano_publicacao = Column(Integer, nullable=True)
    disponivel = Column(Boolean, default=True) # False se estiver emprestado
    
    # Relacionamento reverso (opcional, mas útil)
    emprestimos = relationship("Emprestimo", back_populates="livro")

class Aluno(Base):
    """Tabela de Alunos/Beneficiários"""
    __tablename__ = 'alunos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(100), nullable=False)
    matricula = Column(String(20), unique=True, nullable=False)
    curso = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)

    emprestimos = relationship("Emprestimo", back_populates="aluno")

class Emprestimo(Base):
    """Tabela Transacional de Empréstimos"""
    __tablename__ = 'emprestimos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Chaves Estrangeiras (Relacionamentos)
    livro_id = Column(Integer, ForeignKey('livros.id'), nullable=False)
    aluno_id = Column(Integer, ForeignKey('alunos.id'), nullable=False)
    
    data_retirada = Column(DateTime, default=datetime.now)
    data_devolucao = Column(DateTime, nullable=True) # Null = ainda não devolvido
    status = Column(String(20), default="Ativo") # Ativo, Finalizado
    
    # Relacionamentos para acesso direto ao objeto
    livro = relationship("Livro", back_populates="emprestimos")
    aluno = relationship("Aluno", back_populates="emprestimos")
    
class DadosImportados(Base):
    """Tabela para cumprir o requisito de Importação Web"""
    __tablename__ = 'dados_importados'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    origem_url = Column(String(255))
    conteudo_json = Column(Text) # Armazena o JSON bruto ou processado
    data_importacao = Column(DateTime, default=datetime.now)
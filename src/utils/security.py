import hashlib
import os

def gerar_hash(senha: str) -> str:
    """
    Gera um hash SHA-256 da senha combinada com um salt estático (para fins académicos).
    Em produção, usaríamos um salt aleatório por utilizador.
    """
    salt = "projeto_biblioteca_2025_salt_secreto"
    senha_com_salt = senha + salt
    return hashlib.sha256(senha_com_salt.encode()).hexdigest()

def verificar_senha(senha_digitada: str, hash_armazenado: str) -> bool:
    """Compara a senha digitada com o hash guardado."""
    return gerar_hash(senha_digitada) == hash_armazenado
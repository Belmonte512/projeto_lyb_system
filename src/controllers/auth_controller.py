from src.config import Session
from src.models.entities import Usuario
from src.utils.security import verificar_senha

class AuthController:
    def autenticar(self, username, password):
        """
        Verifica se o utilizador existe e se a senha bate.
        Retorna: O objeto Usuario se sucesso, ou None se falha.
        """
        session = Session()
        try:
            # Busca o usuário pelo nome (case insensitive)
            user = session.query(Usuario).filter(Usuario.username == username).first()
            
            if user and verificar_senha(password, user.senha_hash):
                return user
            return None
        except Exception as e:
            print(f"Erro na autenticação: {e}")
            return None
        finally:
            session.close()
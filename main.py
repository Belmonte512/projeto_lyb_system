import sys
import os
import tkinter as tk
from tkinter import messagebox

# --- Configuração do Path ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# --- Importações ---
from src.config import init_db, Session
from src.models.entities import Usuario
from src.utils.security import gerar_hash
from src.views.login_view import LoginView
from src.views.main_menu_view import MainMenuView 
from src.views.about_view import AboutView
from src.views.books_view import BooksView
from src.views.students_view import StudentsView  
from src.views.loans_view import LoansView 
from src.utils.exporter import DataExporter  
from src.views.import_view import ImportView  # <--- NOVA IMPORTAÇÃO

# --- Lógica de Seed (Admin) ---
def seed_admin():
    session = Session()
    try:
        usuario_existente = session.query(Usuario).first()
        if not usuario_existente:
            admin = Usuario(
                username="admin",
                senha_hash=gerar_hash("admin123"),
                nome_completo="Administrador do Sistema"
            )
            session.add(admin)
            session.commit()
    except Exception:
        pass
    finally:
        session.close()

# --- Aplicação Principal (GUI) ---
class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.current_user = None
        
        init_db()
        seed_admin()
        self.show_login()
        
    def show_login(self):
        self.login_frame = LoginView(self.root, self.on_login_success)
        
    def on_login_success(self, user):
        self.current_user = user
        self.login_frame.destroy()
        self.setup_main_window()

    def setup_main_window(self):
        """Carrega o Menu Principal"""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.geometry("900x600")
        self.root.title(f"Biblioteca - {self.current_user.nome_completo}")
        
        # Dicionário de Ações (O que cada botão faz)
        actions = {
            'livros': self.open_livros,
            'alunos': self.open_alunos,
            'emprestimos': self.open_emprestimos,
            'importar': self.open_importar,
            'exportar': self.run_export,
            'sobre': self.open_sobre,
            'sair': self.logout
        }
        
        # Instancia a View do Menu
        self.menu_frame = MainMenuView(self.root, actions, self.current_user)

    def switch_frame(self, new_frame_class):
        """Método utilitário para trocar o Frame principal da janela."""
        if hasattr(self, 'current_frame'):
            self.current_frame.destroy()

    # O novo frame deve sempre ter o callback para voltar ao menu
        self.current_frame = new_frame_class(self.root, self.setup_main_window)

    # --- PLACEHOLDERS (Funções provisórias) ---
    def open_livros(self):
    # Destruir o menu antes de abrir a nova tela é a abordagem mais limpa
        self.menu_frame.destroy()

    # Passa a classe BooksView e o callback para o menu
        self.current_frame = BooksView(self.root, self.setup_main_window)
        
    def open_alunos(self):
        """Abre a tela de Gestão de Alunos."""
        self.menu_frame.destroy()
        self.current_frame = StudentsView(self.root, self.setup_main_window)

    def open_emprestimos(self):
        """Abre a tela de Gestão de Empréstimos."""
        self.menu_frame.destroy()
        self.current_frame = LoansView(self.root, self.setup_main_window)

    def open_importar(self):
        """Abre a tela de Importação Web."""
        self.menu_frame.destroy()
        self.current_frame = ImportView(self.root, self.setup_main_window)
        
    def run_export(self):
        """Executa a exportação de dados"""
        if messagebox.askyesno("Exportar Dados", "Deseja gerar um backup completo (ZIP) dos dados?"):
            exporter = DataExporter()
            sucesso, mensagem = exporter.exportar_dados()
            
            if sucesso:
                messagebox.showinfo("Backup Concluído", mensagem)
            else:
                messagebox.showerror("Erro no Backup", mensagem)

    def open_sobre(self):
        # Cria e exibe a janela Sobre
        AboutView(self.root)

    def logout(self):
        """Faz logoff e volta para login"""
        if messagebox.askyesno("Sair", "Deseja realmente sair?"):
            self.menu_frame.destroy() # Remove o menu
            self.current_user = None
            self.root.geometry("400x300") # Redimensiona para login
            self.show_login()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
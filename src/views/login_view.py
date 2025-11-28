import tkinter as tk
from tkinter import messagebox
from src.controllers.auth_controller import AuthController

class LoginView(tk.Frame):
    def __init__(self, root, on_login_success_callback):
        """
        root: A janela principal do Tkinter
        on_login_success_callback: Função que será chamada quando o login der certo
        """
        super().__init__(root)
        self.root = root
        self.on_login_success = on_login_success_callback
        self.controller = AuthController()
        
        self.root.title("Sistema de Biblioteca - Login")
        self.root.geometry("500x350")
        self.root.resizable(False, False)
        
        self._setup_ui()
        self.pack(expand=True, fill='both', padx=20, pady=20)

    def _setup_ui(self):
        # Título
        lbl_title = tk.Label(self, text="Acesso Restrito", font=("Arial", 16, "bold"))
        lbl_title.pack(pady=20)

        # Campo Usuário
        lbl_user = tk.Label(self, text="Usuário:")
        lbl_user.pack(anchor='w')
        self.entry_user = tk.Entry(self)
        self.entry_user.pack(fill='x', pady=(0, 10))

        # Campo Senha
        lbl_pass = tk.Label(self, text="Senha:")
        lbl_pass.pack(anchor='w')
        self.entry_pass = tk.Entry(self, show="*") # Oculta caracteres
        self.entry_pass.pack(fill='x', pady=(0, 20))

        # Botão Entrar
        btn_login = tk.Button(self, text="ENTRAR", command=self._realizar_login, 
                              bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_login.pack(fill='x', ipady=5)

        # Bind da tecla Enter
        self.root.bind('<Return>', lambda event: self._realizar_login())

    def _realizar_login(self):
        usuario = self.entry_user.get()
        senha = self.entry_pass.get()

        user_obj = self.controller.autenticar(usuario, senha)

        if user_obj:
            # Sucesso!
            # Limpa os campos (segurança)
            self.entry_pass.delete(0, tk.END)
            # Chama o callback para trocar de tela
            self.on_login_success(user_obj)
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
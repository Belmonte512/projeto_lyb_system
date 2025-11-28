import tkinter as tk
from tkinter import font

class MainMenuView(tk.Frame):
    def __init__(self, root, callbacks, usuario_ativo):
        """
        root: Janela principal
        callbacks: Dicionário com as funções para cada botão {'livros': func, 'alunos': func...}
        usuario_ativo: Objeto do usuário logado para mostrar o nome
        """
        super().__init__(root)
        self.root = root
        self.callbacks = callbacks
        
        # Configuração de Estilo
        self.bg_color = "#f0f0f0"
        self.configure(bg=self.bg_color)
        
        # Título de Boas Vindas
        header_frame = tk.Frame(self, bg="#333", height=80)
        header_frame.pack(fill='x')
        
        lbl_title = tk.Label(header_frame, text="SISTEMA DE BIBLIOTECA", 
                             bg="#333", fg="white", font=("Arial", 18, "bold"))
        lbl_title.pack(side='left', padx=20, pady=20)
        
        lbl_user = tk.Label(header_frame, text=f"Logado como: {usuario_ativo.username}", 
                            bg="#333", fg="#ddd", font=("Arial", 10))
        lbl_user.pack(side='right', padx=20)

        # Container dos Botões (Grid)
        btn_container = tk.Frame(self, bg=self.bg_color)
        btn_container.pack(expand=True, fill='both', padx=50, pady=50)
        
        # Definição dos Botões
        # Texto, Chave do Callback, Cor
        botoes = [
            ("📚 Gerenciar Livros", 'livros', "#2196F3"),
            ("🎓 Gerenciar Alunos", 'alunos', "#009688"),
            ("🤝 Empréstimos", 'emprestimos', "#FF9800"),
            ("⬇️ Importar Dados", 'importar', "#673AB7"),
            ("💾 Exportar (JSON/ZIP)", 'exportar', "#795548"),
            ("ℹ️ Sobre", 'sobre', "#607D8B"),
            ("🚪 Sair", 'sair', "#F44336")
        ]

        # Renderizar botões em Grid (3 colunas)
        row_val = 0
        col_val = 0
        for text, key, color in botoes:
            btn = tk.Button(btn_container, text=text, bg=color, fg="white",
                            font=("Arial", 12, "bold"), height=2, width=20,
                            command=self.callbacks.get(key)) # Pega a função do dicionário
            
            btn.grid(row=row_val, column=col_val, padx=10, pady=10)
            
            col_val += 1
            if col_val > 2: # Quebra linha após 3 botões
                col_val = 0
                row_val += 1

        self.pack(expand=True, fill='both')
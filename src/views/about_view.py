import tkinter as tk
from tkinter import ttk

class AboutView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Sobre o Sistema")
        self.geometry("500x400")
        self.resizable(False, False)
        self.configure(bg="white")
        
        # Torna a janela modal (foca nela e impede clique na de trás)
        self.transient(parent)
        self.grab_set()
        self.focus_set()
        
        self._setup_ui()

    def _setup_ui(self):
        # Cabeçalho
        header = tk.Frame(self, bg="#607D8B", height=60)
        header.pack(fill='x')
        
        lbl_header = tk.Label(header, text="Informações do Projeto", 
                              bg="#607D8B", fg="white", font=("Arial", 14, "bold"))
        lbl_header.pack(pady=15)
        
        # Corpo
        content_frame = tk.Frame(self, bg="white", padx=20, pady=20)
        content_frame.pack(fill='both', expand=True)
        
        # Seção 1: O Projeto
        self._add_section_title(content_frame, "Tema e Objetivo")
        
        txt_projeto = (
            "Tema: Sistema de Gestão de Biblioteca Universitária\n\n"
            "Objetivo: Desenvolver uma aplicação desktop em Python "
            "capaz de gerenciar o acervo de livros, controlar empréstimos "
            "de alunos e garantir a integridade dos dados através de "
            "persistência em banco de dados relacional."
        )
        lbl_proj = tk.Label(content_frame, text=txt_projeto, justify="left", 
                            bg="white", wraplength=440, font=("Arial", 10))
        lbl_proj.pack(anchor='w', pady=(0, 15))
        
        # Seção 2: Desenvolvedores
        self._add_section_title(content_frame, "Equipe de Desenvolvimento")
        
        # --- ATENÇÃO: SUBSTITUA PELOS SEUS DADOS ---
        devs = [
            ("Gabriel Vinicius Pessolo Fiumari", "Matrícula: 2840482413022")
        ]
        
        for nome, mat in devs:
            frame_dev = tk.Frame(content_frame, bg="#f9f9f9", borderwidth=1, relief="solid")
            frame_dev.pack(fill='x', pady=2, ipady=5)
            
            lbl_nome = tk.Label(frame_dev, text=nome, font=("Arial", 10, "bold"), bg="#f9f9f9")
            lbl_nome.pack(side='left', padx=10)
            
            lbl_mat = tk.Label(frame_dev, text=mat, font=("Arial", 9), fg="#555", bg="#f9f9f9")
            lbl_mat.pack(side='right', padx=10)
            
        # Botão Fechar
        btn_close = tk.Button(self, text="Fechar", command=self.destroy, 
                              bg="#607D8B", fg="white", width=15)
        btn_close.pack(pady=20)

    def _add_section_title(self, parent, text):
        lbl = tk.Label(parent, text=text, font=("Arial", 11, "bold"), 
                       bg="white", fg="#333")
        lbl.pack(anchor='w', pady=(5, 2))
        tk.Frame(parent, bg="#ccc", height=1).pack(fill='x', pady=(0, 10)) # Linha separadora
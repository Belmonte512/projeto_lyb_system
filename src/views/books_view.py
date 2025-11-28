import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers.library_controller import LivroController

class BooksView(tk.Frame):
    def __init__(self, root, on_back_callback):
        super().__init__(root)
        self.root = root
        self.on_back = on_back_callback
        self.controller = LivroController()

        self.root.title("Sistema de Biblioteca - Gestão de Livros")
        
        self.pack(expand=True, fill='both')
        self._setup_ui()
        self._load_data() # Carrega os dados na inicialização

    def _setup_ui(self):
        # Frame Principal - Dividido em Listagem (esquerda) e Formulário (direita)
        main_paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned_window.pack(fill='both', expand=True, padx=10, pady=10)

        # --- A. LISTAGEM (Tabela) ---
        list_frame = ttk.Frame(main_paned_window, padding="10")
        main_paned_window.add(list_frame, weight=3) # Ocupa 3/4 da largura
        
        lbl_title = tk.Label(list_frame, text="Acervo da Biblioteca", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=10)

        # Treeview (Tabela)
        columns = ('id', 'titulo', 'autor', 'isbn', 'ano', 'status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Configuração das Colunas
        self.tree.heading('id', text='ID', anchor=tk.W)
        self.tree.column('id', width=40, stretch=tk.NO)
        self.tree.heading('titulo', text='Título')
        self.tree.heading('autor', text='Autor')
        self.tree.heading('isbn', text='ISBN')
        self.tree.heading('ano', text='Ano', anchor=tk.CENTER)
        self.tree.column('ano', width=70, stretch=tk.NO)
        self.tree.heading('status', text='Status')
        self.tree.column('status', width=100, stretch=tk.NO)

        # Scrollbar
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        # Empacotamento
        vsb.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)
        
        # Botões da Tabela
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill='x', pady=10)
        
        btn_refresh = tk.Button(btn_frame, text="⟳ Atualizar", command=self._load_data)
        btn_refresh.pack(side='left', padx=5)

        btn_delete = tk.Button(btn_frame, text="🗑️ Excluir Selecionado", command=self._delete_book, bg="red", fg="white")
        btn_delete.pack(side='left', padx=5)
        
        btn_back = tk.Button(btn_frame, text="⬅️ Menu Principal", command=self._go_back)
        btn_back.pack(side='right', padx=5)
        
        # --- B. FORMULÁRIO (Cadastro/Edição) ---
        form_frame = ttk.Frame(main_paned_window, padding="10")
        main_paned_window.add(form_frame, weight=1) # Ocupa 1/4 da largura

        lbl_form_title = tk.Label(form_frame, text="Cadastrar Novo Livro", font=("Arial", 14, "bold"))
        lbl_form_title.grid(row=0, column=0, columnspan=2, pady=10)

        # Campos do Formulário
        fields = ["Título:", "Autor:", "ISBN:", "Ano:"]
        self.entries = {}
        for i, field in enumerate(fields):
            lbl = tk.Label(form_frame, text=field, anchor='w')
            lbl.grid(row=i+1, column=0, sticky='w', pady=5, padx=5)
            
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i+1, column=1, sticky='ew', pady=5, padx=5)
            self.entries[field.replace(':', '')] = entry
            
        btn_add = tk.Button(form_frame, text="➕ Adicionar Livro", command=self._add_book, 
                            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"))
        btn_add.grid(row=len(fields)+1, column=0, columnspan=2, pady=20, sticky='ew')

    # --- Métodos de Interação com o Controller ---
    
    def _load_data(self):
        """Busca dados no Controller e preenche a Treeview."""
        # Limpa os dados atuais
        for item in self.tree.get_children():
            self.tree.delete(item)

        livros = self.controller.listar_livros()
        
        if not livros:
            self.tree.insert('', tk.END, values=['Nenhum livro encontrado'], tags=('center',))
            return

        for livro in livros:
            self.tree.insert('', tk.END, values=(
                livro['id'], 
                livro['titulo'], 
                livro['autor'], 
                livro['isbn'], 
                livro['ano'], 
                livro['status']
            ))

    def _add_book(self):
        """Lê o formulário e chama o Controller para criar o livro."""
        titulo = self.entries['Título'].get()
        autor = self.entries['Autor'].get()
        isbn = self.entries['ISBN'].get()
        ano = self.entries['Ano'].get()
        
        # Validação básica
        if not titulo or not autor:
            messagebox.showwarning("Atenção", "Título e Autor não podem estar vazios.")
            return

        sucesso, mensagem = self.controller.criar_livro(titulo, autor, isbn, ano)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self._clear_form()
            self._load_data() # Atualiza a tabela
        else:
            messagebox.showerror("Erro de Cadastro", mensagem)

    def _delete_book(self):
        """Obtém o ID selecionado na tabela e chama o Controller para exclusão."""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um livro na tabela para excluir.")
            return

        # Pega o ID da primeira coluna (que é o ID do banco)
        livro_id = self.tree.item(selected_item)['values'][0]

        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o livro ID {livro_id}?"):
            sucesso, mensagem = self.controller.excluir_livro(livro_id)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self._load_data() # Atualiza a tabela
            else:
                messagebox.showerror("Erro de Exclusão", mensagem)

    def _clear_form(self):
        """Limpa todos os campos do formulário."""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def _go_back(self):
        """Volta para a tela principal (Menu)."""
        self.destroy() # Destrói esta view
        self.on_back() # Chama o callback para re-renderizar o menu
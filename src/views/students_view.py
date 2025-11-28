import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers.student_controller import AlunoController

class StudentsView(tk.Frame):
    def __init__(self, root, on_back_callback):
        super().__init__(root)
        self.root = root
        self.on_back = on_back_callback
        self.controller = AlunoController()

        self.root.title("Sistema de Biblioteca - Gestão de Alunos")
        
        self.pack(expand=True, fill='both')
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        main_paned_window = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned_window.pack(fill='both', expand=True, padx=10, pady=10)

        # --- A. LISTAGEM (Tabela) ---
        list_frame = ttk.Frame(main_paned_window, padding="10")
        main_paned_window.add(list_frame, weight=3) 
        
        lbl_title = tk.Label(list_frame, text="Alunos Cadastrados", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=10)

        # Treeview (Tabela)
        columns = ('id', 'nome', 'matricula', 'email', 'emprestimos')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        # Configuração das Colunas
        self.tree.heading('id', text='ID', anchor=tk.W)
        self.tree.column('id', width=40, stretch=tk.NO)
        self.tree.heading('nome', text='Nome Completo')
        self.tree.heading('matricula', text='Matrícula', anchor=tk.CENTER)
        self.tree.column('matricula', width=100, stretch=tk.NO)
        self.tree.heading('email', text='E-mail')
        self.tree.heading('emprestimos', text='Empréstimos Ativos', anchor=tk.CENTER)
        self.tree.column('emprestimos', width=120, stretch=tk.NO)

        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        vsb.pack(side='right', fill='y')
        self.tree.pack(fill='both', expand=True)
        
        # Botões da Tabela
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(btn_frame, text="⟳ Atualizar", command=self._load_data).pack(side='left', padx=5)
        tk.Button(btn_frame, text="🗑️ Excluir Selecionado", command=self._delete_student, 
                  bg="red", fg="white").pack(side='left', padx=5)
        tk.Button(btn_frame, text="⬅️ Menu Principal", command=self._go_back).pack(side='right', padx=5)
        
        # --- B. FORMULÁRIO ---
        form_frame = ttk.Frame(main_paned_window, padding="10")
        main_paned_window.add(form_frame, weight=1)

        lbl_form_title = tk.Label(form_frame, text="Cadastrar Novo Aluno", font=("Arial", 14, "bold"))
        lbl_form_title.grid(row=0, column=0, columnspan=2, pady=10)

        fields = ["Nome Completo:", "Matrícula:", "E-mail:"]
        self.entries = {}
        for i, field in enumerate(fields):
            lbl = tk.Label(form_frame, text=field, anchor='w')
            lbl.grid(row=i+1, column=0, sticky='w', pady=5, padx=5)
            
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i+1, column=1, sticky='ew', pady=5, padx=5)
            self.entries[field.replace(':', '')] = entry
            
        tk.Button(form_frame, text="➕ Adicionar Aluno", command=self._add_student, 
                  bg="#009688", fg="white", font=("Arial", 10, "bold")).grid(
                      row=len(fields)+1, column=0, columnspan=2, pady=20, sticky='ew')

    # --- Métodos de Interação com o Controller ---
    
    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        alunos = self.controller.listar_alunos()
        
        for aluno in alunos:
            self.tree.insert('', tk.END, values=(
                aluno['id'], 
                aluno['nome'], 
                aluno['matricula'], 
                aluno['email'], 
                aluno['emprestimos']
            ))

    def _add_student(self):
        nome = self.entries['Nome Completo'].get()
        matricula = self.entries['Matrícula'].get()
        email = self.entries['E-mail'].get()
        
        sucesso, mensagem = self.controller.criar_aluno(nome, matricula, email)

        if sucesso:
            messagebox.showinfo("Sucesso", mensagem)
            self._clear_form()
            self._load_data()
        else:
            messagebox.showerror("Erro de Cadastro", mensagem)

    def _delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Atenção", "Selecione um aluno na tabela para excluir.")
            return

        aluno_id = self.tree.item(selected_item)['values'][0]

        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir o aluno ID {aluno_id}?"):
            sucesso, mensagem = self.controller.excluir_aluno(aluno_id)
            if sucesso:
                messagebox.showinfo("Sucesso", mensagem)
                self._load_data()
            else:
                messagebox.showerror("Erro de Exclusão", mensagem)

    def _clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def _go_back(self):
        self.destroy()
        self.on_back()
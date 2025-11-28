import tkinter as tk
from tkinter import messagebox, ttk
from src.controllers.loan_controller import EmprestimoController

class LoansView(tk.Frame):
    def __init__(self, root, on_back_callback):
        super().__init__(root)
        self.root = root
        self.on_back = on_back_callback
        self.controller = EmprestimoController()

        self.root.title("Sistema de Biblioteca - Gestão de Empréstimos")
        
        # Variável para controle do filtro (Ativo/Finalizado)
        self.filter_var = tk.StringVar(value="Ativo")
        
        self.pack(expand=True, fill='both')
        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        main_paned = ttk.PanedWindow(self, orient=tk.HORIZONTAL)
        main_paned.pack(fill='both', expand=True, padx=10, pady=10)

        # --- A. LISTAGEM (Esquerda) ---
        list_frame = ttk.Frame(main_paned, padding="10")
        main_paned.add(list_frame, weight=3)
        
        # Cabeçalho com Filtro
        header_frame = tk.Frame(list_frame)
        header_frame.pack(fill='x', pady=10)
        
        tk.Label(header_frame, text="Controle de Empréstimos", font=("Arial", 14, "bold")).pack(side='left')
        
        # Radio buttons para filtrar
        frame_filter = tk.Frame(header_frame)
        frame_filter.pack(side='right')
        tk.Radiobutton(frame_filter, text="Em Aberto", variable=self.filter_var, 
                       value="Ativo", command=self._load_data).pack(side='left', padx=5)
        tk.Radiobutton(frame_filter, text="Histórico", variable=self.filter_var, 
                       value="Finalizado", command=self._load_data).pack(side='left', padx=5)

        # Tabela
        columns = ('id', 'livro', 'aluno', 'retirada', 'devolucao', 'status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        
        self.tree.heading('id', text='ID')
        self.tree.column('id', width=30)
        self.tree.heading('livro', text='Livro')
        self.tree.heading('aluno', text='Aluno')
        self.tree.heading('retirada', text='Data Retirada')
        self.tree.column('retirada', width=100)
        self.tree.heading('devolucao', text='Data Devolução')
        self.tree.column('devolucao', width=100)
        self.tree.heading('status', text='Status')
        self.tree.column('status', width=80)

        self.tree.pack(fill='both', expand=True)
        
        # Botões de Ação da Tabela
        btn_frame = ttk.Frame(list_frame)
        btn_frame.pack(fill='x', pady=10)
        
        tk.Button(btn_frame, text="⟳ Atualizar", command=self._load_data).pack(side='left')
        tk.Button(btn_frame, text="⬅️ Voltar ao Menu", command=self._go_back).pack(side='right')
        
        # Botão de Devolução (Destaque)
        tk.Button(btn_frame, text="✅ Registrar Devolução", command=self._return_loan, 
                  bg="#FF9800", fg="white").pack(side='left', padx=20)

        # --- B. FORMULÁRIO DE NOVO EMPRÉSTIMO (Direita) ---
        form_frame = ttk.Frame(main_paned, padding="10", relief="solid", borderwidth=1)
        main_paned.add(form_frame, weight=1)

        tk.Label(form_frame, text="Novo Empréstimo", font=("Arial", 12, "bold")).pack(pady=10)
        
        tk.Label(form_frame, text="Matrícula do Aluno:", anchor='w').pack(fill='x', pady=(10,0))
        self.entry_matricula = tk.Entry(form_frame)
        self.entry_matricula.pack(fill='x', pady=5)
        
        tk.Label(form_frame, text="ISBN do Livro:", anchor='w').pack(fill='x', pady=(10,0))
        self.entry_isbn = tk.Entry(form_frame)
        self.entry_isbn.pack(fill='x', pady=5)
        
        tk.Button(form_frame, text="🚀 Confirmar Saída", command=self._create_loan,
                  bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), height=2).pack(fill='x', pady=30)
        
        tk.Label(form_frame, text="Nota: Certifique-se de que o livro\nestá disponível e a matrícula correta.", 
                 fg="gray", font=("Arial", 8)).pack(side='bottom')

    def _load_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        status_filter = self.filter_var.get()
        emprestimos = self.controller.listar_emprestimos(status=status_filter)
        
        for e in emprestimos:
            self.tree.insert('', tk.END, values=(
                e['id'], e['livro_titulo'], e['aluno_nome'], 
                e['data_retirada'], e['data_devolucao'], e['status']
            ))

    def _create_loan(self):
        matricula = self.entry_matricula.get()
        isbn = self.entry_isbn.get()
        
        if not matricula or not isbn:
            messagebox.showwarning("Atenção", "Preencha a Matrícula e o ISBN.")
            return
            
        sucesso, msg = self.controller.realizar_emprestimo(matricula, isbn)
        
        if sucesso:
            messagebox.showinfo("Sucesso", msg)
            self.entry_matricula.delete(0, tk.END)
            self.entry_isbn.delete(0, tk.END)
            self.filter_var.set("Ativo") # Força visualização dos ativos
            self._load_data()
        else:
            messagebox.showerror("Erro", msg)

    def _return_loan(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione um empréstimo na lista para devolver.")
            return
            
        item = self.tree.item(selected)
        loan_id = item['values'][0]
        status = item['values'][5]
        
        if status == "Finalizado":
            messagebox.showinfo("Info", "Este empréstimo já foi finalizado.")
            return
            
        if messagebox.askyesno("Confirmar Devolução", f"Confirmar devolução do empréstimo ID {loan_id}?"):
            sucesso, msg = self.controller.realizar_devolucao(loan_id)
            if sucesso:
                messagebox.showinfo("Sucesso", msg)
                self._load_data()
            else:
                messagebox.showerror("Erro", msg)

    def _go_back(self):
        self.destroy()
        self.on_back()
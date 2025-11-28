import tkinter as tk
from tkinter import messagebox, ttk
from src.utils.importer import WebImporter
from src.controllers.student_controller import AlunoController

class ImportView(tk.Frame):
    def __init__(self, root, on_back_callback):
        super().__init__(root)
        self.root = root
        self.on_back = on_back_callback
        self.importer = WebImporter()

        self.aluno_controller = AlunoController()

        self.root.title("Sistema de Biblioteca - Importação de Dados Externos")
        self.pack(expand=True, fill='both')
        
        self._setup_ui()
        # Tenta carregar dados anteriores se houver
        self._load_from_db()

    def _setup_ui(self):
        # Cabeçalho
        header = tk.Frame(self, bg="#673AB7", height=60)
        header.pack(fill='x')
        
        lbl_title = tk.Label(header, text="Integração Web (API Externa)", 
                             bg="#673AB7", fg="white", font=("Arial", 14, "bold"))
        lbl_title.pack(pady=15)

        # Barra de Ações
        action_frame = tk.Frame(self, pady=10)
        action_frame.pack(fill='x')
        
        btn_import = tk.Button(action_frame, text="⬇️ Baixar Dados da Web", 
                               command=self._run_import,
                               bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        btn_import.pack(side='left', padx=20)

        btn_promote = tk.Button(action_frame, text="Cadastrar como aluno",
                                command=self._promover_para_aluno,
                                bg="#FF9800", fg="white", font=("Arial", 10, "bold"))
        btn_promote.pack(side='left', padx=10)
        
        self.lbl_status = tk.Label(action_frame, text="Status: Aguardando ação...", fg="gray")
        self.lbl_status.pack(side='left', padx=10)
        
        btn_back = tk.Button(action_frame, text="⬅️ Voltar ao Menu", command=self._go_back)
        btn_back.pack(side='right', padx=20)

        # Tabela de Visualização
        tree_frame = ttk.Frame(self, padding="10")
        tree_frame.pack(fill='both', expand=True)
        
        columns = ('id', 'nome', 'username', 'email', 'cidade')
        self.tree = ttk.Treeview(tree_frame, columns=columns, show='headings')
        
        self.tree.heading('id', text='ID Ext.')
        self.tree.column('id', width=50)
        self.tree.heading('nome', text='Nome')
        self.tree.heading('username', text='Usuário')
        self.tree.heading('email', text='E-mail')
        self.tree.column('email', width=200)
        self.tree.heading('cidade', text='Cidade')

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=vsb.set)
        
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')

    def _promover_para_aluno(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Atenção", "Selecione uma pessoa na lista para cadastrar.")
            return
        
        item = self.tree.item(selected)
        dados = item['values']

        nome_importado = dados[1]
        email_importado = dados[3]
        matricula_gerada = f"IMP-{dados[0]}"

        if messagebox.askyesno("Confirmar Integração",
                               f"Deseja cadastrar '{nome_importado}' como aluno oficial?\n"
                               f"Matrícula gerada: {matricula_gerada}"):
            
            sucesso, msg = self.aluno_controller.criar_aluno(
                nome=nome_importado,
                matricula=matricula_gerada,
                email=email_importado
                # curso será vazio/null
            )

            if sucesso:
                messagebox.showinfo("Integração Realizada", f"Sucesso! {nome_importado} agora é um aluno do sistema.")
            else:
                messagebox.showerror("Erro na Integração", msg)

    def _run_import(self):
        self.lbl_status.config(text="Status: Conectando...", fg="blue")
        self.root.update_idletasks() # Força atualização da UI
        
        sucesso, dados, msg = self.importer.importar_dados_externos()
        
        if sucesso:
            self.lbl_status.config(text=f"Status: Sucesso! {len(dados)} registros.", fg="green")
            self._populate_table(dados)
            messagebox.showinfo("Importação Web", msg)
        else:
            self.lbl_status.config(text="Status: Erro na conexão.", fg="red")
            messagebox.showerror("Erro", msg)

    def _load_from_db(self):
        """Carrega o último histórico salvo, se existir."""
        dados, data = self.importer.recuperar_ultimo_import()
        if dados:
            self.lbl_status.config(text=f"Status: Dados recuperados de {data}", fg="gray")
            self._populate_table(dados)

    def _populate_table(self, dados):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for row in dados:
            # Mapeando o JSON do JSONPlaceholder para nossas colunas
            # O JSON vem como: {'id': 1, 'name': '...', 'address': {'city': '...'}, ...}
            cidade = row.get('address', {}).get('city', 'N/A')
            
            self.tree.insert('', tk.END, values=(
                row.get('id'),
                row.get('name'),
                row.get('username'),
                row.get('email'),
                cidade
            ))

    def _go_back(self):
        self.destroy()
        self.on_back()
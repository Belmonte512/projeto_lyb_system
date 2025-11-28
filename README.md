# 📚 LybSystem - Sistema de Gestão de Biblioteca

> **Status do Projeto:** 🚀 Concluído (v1.0)

## 🎯 Sobre o Projeto

O **LybSystem** é uma aplicação desktop desenvolvida em Python para o gerenciamento de bibliotecas acadêmicas. O projeto foi construído com foco estrito em **Arquitetura de Software**, utilizando o padrão **MVC (Model-View-Controller)** para garantir desacoplamento, escalabilidade e manutenibilidade do código.

O sistema gerencia o ciclo completo de empréstimos, desde o cadastro de acervo e alunos até a validação de regras de negócio para retirada e devolução de livros, incluindo integração com APIs externas e persistência relacional.

---

## 🛠️ Tecnologias e Arquitetura

O projeto foi desenvolvido seguindo as melhores práticas de Engenharia de Software:

* **Linguagem:** Python 3.10+
* **Interface Gráfica (GUI):** Tkinter (Nativo)
* **Persistência (ORM):** SQLAlchemy
* **Banco de Dados:** SQLite (Portável)
* **Integração Web:** Requests
* **Segurança:** Hashlib (SHA-256 com Salt)

### Destaques Arquiteturais
* **Padrão MVC:** Separação clara entre Lógica de Negócio (`controllers`), Interface (`views`) e Dados (`models`).
* **Repository Pattern:** Abstração das operações de banco de dados via SQLAlchemy.
* **Tratamento de Exceções:** Gestão robusta de erros para garantir que a aplicação não feche inesperadamente.
* **Transações Atômicas:** Garantia de integridade nos empréstimos (o livro só fica indisponível se o empréstimo for confirmado).

---

## ⚙️ Funcionalidades Principais

### 🔐 Autenticação e Segurança
* Login com validação de credenciais.
* Armazenamento de senhas utilizando Hashing (não armazena texto plano).
* Controle de sessão de usuário.

### 📚 Gestão de Acervo (Livros)
* CRUD completo (Criar, Ler, Atualizar, Deletar).
* Visualização em tabela (`Treeview`) com barra de rolagem.
* Controle de status de disponibilidade (Disponível/Emprestado).

### 🎓 Gestão de Membros (Alunos)
* Cadastro com validação de matrícula única.
* Bloqueio de exclusão de alunos que possuem débitos (empréstimos ativos).

### 🤝 Motor de Empréstimos (Core Business)
* Realização de empréstimos com validação de estoque e existência de cadastro.
* Devolução de livros com atualização automática de status no acervo.
* Histórico de transações (Ativos vs. Finalizados).

### 🔄 Integração e Portabilidade
* **Exportação:** Backup completo dos dados em formato JSON, compactado automaticamente em ZIP.
* **Importação Web:** Integração com API externa (JSONPlaceholder) para simulação de carga de dados via HTTP.

---

## 📂 Estrutura do Projeto

```text
projeto_lyb_system/
│
├── data/                   # Arquivos de banco de dados (.db) e exports (.zip)
├── src/
│   ├── config.py           # Configurações de Conexão e Sessão DB
│   ├── models/             # Entidades ORM (Tabelas)
│   ├── views/              # Interfaces Gráficas (Tkinter)
│   ├── controllers/        # Regras de Negócio e Orquestração
│   └── utils/              # Ferramentas (Security, Exporter, Importer)
├── main.py                 # Ponto de Entrada (Entry Point)
└── requirements.txt        # Dependências do Projeto

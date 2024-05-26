import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
from hashlib import sha256
import random

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Sistema de Loja")
        self.root.configure(bg="#2c3e50")  # Background cinza escuro

        # Pegar as dimensões da tela do usuário
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()

        # Aumentar o tamanho da janela
        largura_janela = int(largura_tela * 0.4)  # Aumentando a largura
        altura_janela = int(altura_tela * 0.4)  # Aumentando a altura

        # Centralizar a janela na tela
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2

        self.root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        self.root.resizable(False, False)

        # Frame para centralizar os widgets
        frame = tk.Frame(self.root, bg="#2c3e50")  # Background cinza escuro
        frame.pack(expand=True)

        # Elementos da interface de login
        self.label_username = tk.Label(frame, text="Username:", bg="#2c3e50", fg="white")  # Texto branco
        self.label_username.pack(pady=10)
        self.entry_username = tk.Entry(frame)
        self.entry_username.pack(pady=5)

        self.label_password = tk.Label(frame, text="Password:", bg="#2c3e50", fg="white")  # Texto branco
        self.label_password.pack(pady=10)
        self.entry_password = tk.Entry(frame, show="*")
        self.entry_password.pack(pady=5)

        self.btn_login = tk.Button(frame, text="Login", command=self.login, bg="#16a085", fg="white")  # Botão verde
        self.btn_login.pack(pady=10)

        # Botão para limpar informações
        self.btn_limpar = tk.Button(frame, text="Limpar", command=self.limpar_campos, bg="#c0392b", fg="white")  # Botão vermelho
        self.btn_limpar.pack(pady=5)

        # Conectar ao banco de dados
        try:
            self.conn = sqlite3.connect('loja.db')
            self.c = self.conn.cursor()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
            self.root.destroy()

        # Criar tabelas e inserir dados fictícios
        self.criar_tabela_usuarios()
        self.criar_tabela_produtos()

    def criar_tabela_usuarios(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS usuarios
                              (id INTEGER PRIMARY KEY,
                               username TEXT,
                               password TEXT)''')
            self.conn.commit()
            
            # Inserir usuários fictícios
            self.verificar_inserir_usuarios_ficticios()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar tabela de usuários: {e}")

    def criar_tabela_produtos(self):
        try:
            self.c.execute('''CREATE TABLE IF NOT EXISTS produtos
                              (id INTEGER PRIMARY KEY,
                               nome TEXT,
                               categoria TEXT,
                               preco REAL)''')
            self.conn.commit()
            
            # Inserir produtos fictícios
            self.verificar_inserir_produtos_ficticios()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar tabela de produtos: {e}")

    def verificar_inserir_usuarios_ficticios(self):
        try:
            self.c.execute("SELECT COUNT(*) FROM usuarios")
            count = self.c.fetchone()[0]

            if count == 0:
                # Inserir usuários fictícios 
                usuarios_ficticios = [
                    ("Guilherme", "G123"),
                    ("Isaac", "I123"),
                    ("Romario", "R123")
                ]
                
                for username, password in usuarios_ficticios:
                    hashed_password = sha256(password.encode()).hexdigest()
                    self.c.execute("INSERT INTO usuarios (username, password) VALUES (?, ?)", (username, hashed_password))
                
                self.conn.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir usuários fictícios: {e}")

    def verificar_inserir_produtos_ficticios(self):
        try:
            self.c.execute("SELECT COUNT(*) FROM produtos")
            count = self.c.fetchone()[0]

            if count == 0:
                # Inserir produtos fictícios
                marcas = ["Samsung", "Apple", "Xiaomi", "Sony", "LG"]
                categorias = ["Carregador de Celular", "Capa para Celular", "Fone com Fio", "Fone sem Fio", "Adaptador de Entrada"]
                precos = [29.90, 19.90, 49.90, 99.90, 149.90, 199.90]

                produtos_ficticios = []
                for i in range(100):
                    marca = random.choice(marcas)
                    categoria = random.choice(categorias)
                    preco = random.choice(precos)
                    nome = f"{categoria[:-1]} {marca}"  # Remove o "s" para singularizar o nome da categoria
                    produtos_ficticios.append((nome, categoria, preco))

                for nome, categoria, preco in produtos_ficticios:
                    self.c.execute("INSERT INTO produtos (nome, categoria, preco) VALUES (?, ?, ?)", (nome, categoria, preco))
                
                self.conn.commit()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir produtos fictícios: {e}")

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        try:
            hashed_password = sha256(password.encode()).hexdigest()
            self.c.execute("SELECT * FROM usuarios WHERE username=? AND password=?", (username, hashed_password))
            user = self.c.fetchone()

            if user:
                messagebox.showinfo("Sucesso", "Login bem-sucedido!")
                self.root.destroy()
                self.open_main_app()
            else:
                messagebox.showerror("Erro", "Credenciais inválidas.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao fazer login: {e}")

    def open_main_app(self):
        root = tk.Tk()
        app = LojaApp(root, self.conn)
        root.title("Sistema de Loja")
        root.configure(bg="#2c3e50")  # Background cinza escuro
        
        # Pegar as dimensões da tela do usuário
        largura_tela = root.winfo_screenwidth()
        altura_tela = root.winfo_screenheight()

        # Aumentar o tamanho da janela
        largura_janela = int(largura_tela * 0.7)  # Aumentando a largura
        altura_janela = int(altura_tela * 0.7)  # Aumentando a altura

        # Centralizar a janela na tela
        pos_x = (largura_tela - largura_janela) // 2
        pos_y = (altura_tela - altura_janela) // 2

        root.geometry(f"{largura_janela}x{altura_janela}+{pos_x}+{pos_y}")
        root.resizable(False, False)

        root.mainloop()

    def limpar_campos(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

class LojaApp:
    def __init__(self, root, conn):
        self.root = root
        self.conn = conn
        self.produtos = []
        self.produto_selecionado = None

        self.root.configure(bg="#2c3e50")  # Background cinza escuro

        self.create_widgets()
        self.exibir_produtos()

    def create_widgets(self):
        # Configurar o grid layout
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Frame para centralizar os widgets
        frame = tk.Frame(self.root, bg="#2c3e50")  # Background cinza escuro
        frame.grid(sticky="nsew", padx=10, pady=10)

        for i in range(3):
            frame.columnconfigure(i, weight=1)
        frame.rowconfigure(8, weight=1)

        # Elementos da interface principal da loja
        self.label_nome = tk.Label(frame, text="Nome do Produto:", bg="#2c3e50", fg="white")  # Texto branco
        self.label_nome.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="e")  # Ajuste de espaço vertical
        self.entry_nome = tk.Entry(frame)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.label_categoria = tk.Label(frame, text="Categoria:", bg="#2c3e50", fg="white")  # Texto branco
        self.label_categoria.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        
        self.categorias = ["Carregador de Celular", "Capa para Celular", "Fone com Fio", "Fone sem Fio", "Adaptador de Entrada"]
        self.combobox_categoria = ttk.Combobox(frame, values=self.categorias)
        self.combobox_categoria.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.label_preco = tk.Label(frame, text="Preço:", bg="#2c3e50", fg="white")  # Texto branco
        self.label_preco.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_preco = tk.Entry(frame)
        self.entry_preco.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.label_pesquisa = tk.Label(frame, text="Pesquisar:", bg="#2c3e50", fg="white")  # Texto branco
        self.label_pesquisa.grid(row=4, column=0, padx=5, pady=(20, 5), sticky="e")  # Ajuste de espaço vertical
        self.entry_pesquisa = tk.Entry(frame)
        self.entry_pesquisa.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        self.btn_pesquisar = tk.Button(frame, text="Pesquisar", command=self.pesquisar_produto, bg="#16a085", fg="white")  # Botão verde
        self.btn_pesquisar.grid(row=4, column=2, padx=5, pady=5, sticky="ew")

        self.btn_adicionar = tk.Button(frame, text="Adicionar Produto", command=self.adicionar_produto, bg="#16a085", fg="white")  # Botão verde
        self.btn_adicionar.grid(row=5, column=0, padx=5, pady=5)

        self.btn_editar = tk.Button(frame, text="Editar Produto", command=self.editar_produto, bg="#16a085", fg="white")  # Botão verde
        self.btn_editar.grid(row=5, column=1, padx=5, pady=5)

        self.btn_remover = tk.Button(frame, text="Remover Produto", command=self.remover_produto, bg="#16a085", fg="white")  # Botão verde
        self.btn_remover.grid(row=5, column=2, padx=5, pady=5)

        self.table = ttk.Treeview(frame, columns=("Nome", "Categoria", "Preço"), show="headings")
        self.table.heading("Nome", text="Nome")
        self.table.heading("Categoria", text="Categoria")
        self.table.heading("Preço", text="Preço")
        self.table.bind("<ButtonRelease-1>", self.selecionar_produto)
        self.table_scroll = ttk.Scrollbar(frame, orient="vertical", command=self.table.yview)
        self.table.configure(yscrollcommand=self.table_scroll.set)
        self.table.grid(row=6, column=0, columnspan=3, padx=5, pady=(5, 20), sticky="nsew")  # Ajuste de espaço vertical
        self.table_scroll.grid(row=6, column=3, sticky="ns")  # Adicionando a barra de rolagem

        # Adicionando um preenchimento vertical ao grid do Treeview para ocupar o espaço extra
        frame.rowconfigure(6, weight=1)

    def exibir_produtos(self):
        try:
            # Limpar a tabela de produtos antes de exibir novamente
            for row in self.table.get_children():
                self.table.delete(row)
            
            # Consultar produtos no banco de dados e exibir na tabela
            c = self.conn.cursor()
            c.execute("SELECT * FROM produtos")
            self.produtos = c.fetchall()
            
            for produto in self.produtos:
                self.table.insert("", "end", values=(produto[1], produto[2], produto[3]))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exibir produtos: {e}")

    def pesquisar_produto(self):
        try:
            termo_pesquisa = self.entry_pesquisa.get().lower()

            produtos_encontrados = [produto for produto in self.produtos if termo_pesquisa in produto[1].lower()]

            # Limpar a tabela de produtos antes de exibir os resultados da pesquisa
            for row in self.table.get_children():
                self.table.delete(row)

            # Exibir os produtos encontrados na tabela
            for produto in produtos_encontrados:
                self.table.insert("", "end", values=(produto[1], produto[2], produto[3]))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao pesquisar produto: {e}")

    def selecionar_produto(self, event):
        try:
            item_selecionado = self.table.item(self.table.selection())
            self.produto_selecionado = None

            for produto in self.produtos:
                if produto[1] == item_selecionado['values'][0]:
                    self.produto_selecionado = produto
                    break

            self.mostrar_detalhes_produto_selecionado()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao selecionar produto: {e}")

    def mostrar_detalhes_produto_selecionado(self):
        if self.produto_selecionado:
            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, self.produto_selecionado[1])

            self.combobox_categoria.set(self.produto_selecionado[2])

            self.entry_preco.delete(0, tk.END)
            self.entry_preco.insert(0, self.produto_selecionado[3])

    def adicionar_produto(self):
        nome = self.entry_nome.get()
        categoria = self.combobox_categoria.get()
        preco = self.entry_preco.get()

        if nome and categoria and preco:
            c = self.conn.cursor()
            c.execute("INSERT INTO produtos (nome, categoria, preco) VALUES (?, ?, ?)", (nome, categoria, preco))
            self.conn.commit()
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso!")
            self.limpar_campos()
            self.exibir_produtos()
        else:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")

    def editar_produto(self):
        if self.produto_selecionado:
            novo_nome = self.entry_nome.get()
            nova_categoria = self.combobox_categoria.get()
            novo_preco = self.entry_preco.get()

            if novo_nome and nova_categoria and novo_preco:
                c = self.conn.cursor()
                c.execute("UPDATE produtos SET nome=?, categoria=?, preco=? WHERE id=?", (novo_nome, nova_categoria, novo_preco, self.produto_selecionado[0]))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
                self.limpar_campos()
                self.exibir_produtos()
            else:
                messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        else:
            messagebox.showerror("Erro", "Selecione um produto para editar.")

    def remover_produto(self):
        if self.produto_selecionado:
            if messagebox.askyesno("Confirmar", "Tem certeza que deseja remover este produto?"):
                c = self.conn.cursor()
                c.execute("DELETE FROM produtos WHERE id=?", (self.produto_selecionado[0],))
                self.conn.commit()
                messagebox.showinfo("Sucesso", "Produto removido com sucesso!")
                self.limpar_campos()
                self.exibir_produtos()
        else:
            messagebox.showerror("Erro", "Selecione um produto para remover.")

    def limpar_campos(self):
        self.entry_nome.delete(0, tk.END)
        self.combobox_categoria.set("")
        self.entry_preco.delete(0, tk.END)

root = tk.Tk()
app = LoginApp(root)
root.mainloop()
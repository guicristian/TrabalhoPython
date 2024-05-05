import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3

class LojaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Loja")
        
        try:
            self.conn = sqlite3.connect('loja.db')
            self.c = self.conn.cursor()
            
            self.c.execute('''CREATE TABLE IF NOT EXISTS produtos
                                (id INTEGER PRIMARY KEY,
                                nome TEXT,
                                categoria TEXT,
                                preco REAL)''')

            # produtos no estoque
            produtos_teste = [
                ("Carregador USB", "Carregadores de Celular", 19.99),
                ("Carregador de Parede", "Carregadores de Celular", 15.99),
                ("Capa Protetora", "Capas para Celular", 12.99),
                ("Capa de Silicone", "Capas para Celular", 9.99),
                ("Fone de Ouvido com Fio", "Fones com Fio", 29.99),
                ("Fone de Ouvido com Microfone", "Fones com Fio", 24.99),
                ("Fone de Ouvido Bluetooth", "Fones sem Fio", 49.99),
                ("Fone de Ouvido Bluetooth Esportivo", "Fones sem Fio", 39.99),
                ("Adaptador HDMI", "Adaptadores de Entrada", 9.99),
                ("Adaptador VGA", "Adaptadores de Entrada", 7.99)
            ]

            for produto in produtos_teste:
                self.c.execute("INSERT INTO produtos (nome, categoria, preco) VALUES (?, ?, ?)", produto)

            self.conn.commit()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
            self.root.destroy()
            return
        
        self.create_widgets()
        self.exibir_produtos()
    
    def create_widgets(self):
        self.label_nome = tk.Label(self.root, text="Nome do Produto:")
        self.label_nome.grid(row=0, column=0, padx=5, pady=5)
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)

        self.label_categoria = tk.Label(self.root, text="Categoria:")
        self.label_categoria.grid(row=1, column=0, padx=5, pady=5)
        
        self.categorias = ["Carregadores de Celular", "Capas para Celular", "Fones com Fio", "Fones sem Fio", "Adaptadores de Entrada"]
        self.combobox_categoria = ttk.Combobox(self.root, values=self.categorias)
        self.combobox_categoria.grid(row=1, column=1, padx=5, pady=5)

        self.label_preco = tk.Label(self.root, text="Preço:")
        self.label_preco.grid(row=2, column=0, padx=5, pady=5)
        self.entry_preco = tk.Entry(self.root)
        self.entry_preco.grid(row=2, column=1, padx=5, pady=5)

        self.opcao_var = tk.StringVar()
        self.opcao_var.set("adicionar") 
        self.radio_adicionar = tk.Radiobutton(self.root, text="Adicionar Produto", variable=self.opcao_var, value="adicionar")
        self.radio_adicionar.grid(row=3, column=0, padx=5, pady=5)
        self.radio_editar = tk.Radiobutton(self.root, text="Editar Produto", variable=self.opcao_var, value="editar")
        self.radio_editar.grid(row=3, column=1, padx=5, pady=5)
        self.radio_remover = tk.Radiobutton(self.root, text="Remover Produto", variable=self.opcao_var, value="remover")
        self.radio_remover.grid(row=3, column=2, padx=5, pady=5)

        self.btn_confirmar = tk.Button(self.root, text="Confirmar", command=self.executar_acao)
        self.btn_confirmar.grid(row=4, column=0, columnspan=3, padx=5, pady=5)

        self.table = ttk.Treeview(self.root, columns=("Nome", "Categoria", "Preço"))
        self.table.heading("#0", text="ID")
        self.table.heading("Nome", text="Nome")
        self.table.heading("Categoria", text="Categoria")
        self.table.heading("Preço", text="Preço")
        self.table.bind("<ButtonRelease-1>", self.selecionar_produto)
        self.table.grid(row=5, column=0, columnspan=3, padx=5, pady=5)
    
    def exibir_produtos(self):
        try:
            for row in self.table.get_children():
                self.table.delete(row)
            
            self.c.execute("SELECT * FROM produtos")
            produtos = self.c.fetchall()
            
            for produto in produtos:
                self.table.insert("", "end", text=produto[0], values=(produto[1], produto[2], produto[3]))
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exibir produtos: {e}")

    def adicionar_produto(self):
        try:
            nome = self.entry_nome.get()
            categoria = self.combobox_categoria.get()
            preco = float(self.entry_preco.get())
            
            self.c.execute("INSERT INTO produtos (nome, categoria, preco) VALUES (?, ?, ?)", (nome, categoria, preco))
            self.conn.commit()
            
            messagebox.showinfo("Sucesso", "Produto adicionado com sucesso.")
            self.exibir_produtos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao adicionar produto: {e}")

    def editar_produto(self):
        try:
            item = self.table.selection()[0]
            id_produto = self.table.item(item, "text")
            
            nome = self.entry_nome.get()
            categoria = self.combobox_categoria.get()
            preco = float(self.entry_preco.get())
            
            self.c.execute("UPDATE produtos SET nome=?, categoria=?, preco=? WHERE id=?", (nome, categoria, preco, id_produto))
            self.conn.commit()
            
            messagebox.showinfo("Sucesso", "Produto editado com sucesso.")
            self.exibir_produtos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao editar produto: {e}")

    def remover_produto(self):
        try:
            item = self.table.selection()[0]
            id_produto = self.table.item(item, "text")
            
            self.c.execute("DELETE FROM produtos WHERE id=?", (id_produto,))
            self.conn.commit()
            
            messagebox.showinfo("Sucesso", "Produto removido com sucesso.")
            self.exibir_produtos()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao remover produto: {e}")

    def selecionar_produto(self, event):
        try:
            item = self.table.selection()[0]
            id_produto = self.table.item(item, "text")
            nome_produto = self.table.item(item, "values")[0]
            categoria_produto = self.table.item(item, "values")[1]
            preco_produto = self.table.item(item, "values")[2]

            self.entry_nome.delete(0, tk.END)
            self.entry_nome.insert(0, nome_produto)
            self.combobox_categoria.set(categoria_produto)
            self.entry_preco.delete(0, tk.END)
            self.entry_preco.insert(0, preco_produto)
        except IndexError:
            pass

    def executar_acao(self):
        acao = self.opcao_var.get()
        
        if acao == "adicionar":
            self.adicionar_produto()
        elif acao == "editar":
            self.editar_produto()
        elif acao == "remover":
            self.remover_produto()

if __name__ == "__main__":
    root = tk.Tk()
    app = LojaApp(root)
    root.mainloop()

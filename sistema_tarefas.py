import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import json
import os
from datetime import datetime

USERS_FILE = 'usuarios.json'
TASKS_FILE = 'tarefas.json'

# Utilitários
def carregar_dados(caminho):
    if not os.path.exists(caminho):
        return {}
    with open(caminho, 'r') as f:
        return json.load(f)

def salvar_dados(caminho, dados):
    with open(caminho, 'w') as f:
        json.dump(dados, f, indent=4)

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Interface
class SistemaTarefas:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Tarefas Pessoais")
        self.usuario_logado = None
        self.tela_login()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def tela_login(self):
        self.limpar_tela()
        tk.Label(self.root, text="Login", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Email:").pack()
        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack()

        tk.Label(self.root, text="Senha:").pack()
        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.pack()

        tk.Button(self.root, text="Entrar", command=self.login).pack(pady=5)
        tk.Button(self.root, text="Cadastrar", command=self.tela_cadastro).pack()

    def tela_cadastro(self):
        self.limpar_tela()
        tk.Label(self.root, text="Cadastro", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Nome:").pack()
        self.entry_nome = tk.Entry(self.root)
        self.entry_nome.pack()

        tk.Label(self.root, text="Email:").pack()
        self.entry_email = tk.Entry(self.root)
        self.entry_email.pack()

        tk.Label(self.root, text="Senha:").pack()
        self.entry_senha = tk.Entry(self.root, show="*")
        self.entry_senha.pack()

        tk.Button(self.root, text="Cadastrar", command=self.cadastrar).pack(pady=5)
        tk.Button(self.root, text="Voltar", command=self.tela_login).pack()

    def login(self):
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()
        usuarios = carregar_dados(USERS_FILE)

        if email in usuarios and usuarios[email]['senha'] == hash_senha(senha):
            self.usuario_logado = email
            self.tela_menu()
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos.")

    def cadastrar(self):
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        senha = self.entry_senha.get().strip()

        usuarios = carregar_dados(USERS_FILE)
        if email in usuarios:
            messagebox.showerror("Erro", "Usuário já cadastrado.")
            return

        usuarios[email] = {
            "nome": nome,
            "senha": hash_senha(senha)
        }

        salvar_dados(USERS_FILE, usuarios)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
        self.tela_login()

    def tela_menu(self):
        self.limpar_tela()
        tk.Label(self.root, text="Menu de Tarefas", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Adicionar Tarefa", width=25, command=self.adicionar_tarefa).pack(pady=5)
        tk.Button(self.root, text="Listar Tarefas", width=25, command=self.listar_tarefas).pack(pady=5)
        tk.Button(self.root, text="Excluir Tarefa", width=25, command=self.excluir_tarefa).pack(pady=5)
        tk.Button(self.root, text="Sair", width=25, command=self.tela_login).pack(pady=5)

    def adicionar_tarefa(self):
        tarefas = carregar_dados(TASKS_FILE)
        if self.usuario_logado not in tarefas:
            tarefas[self.usuario_logado] = []

        titulo = simpledialog.askstring("Tarefa", "Título:")
        if not titulo: return
        descricao = simpledialog.askstring("Tarefa", "Descrição:")
        data = simpledialog.askstring("Tarefa", "Data (DD/MM/AAAA):")
        hora = simpledialog.askstring("Tarefa", "Hora (HH:MM):")
        categoria = simpledialog.askstring("Tarefa", "Categoria:")

        nova_tarefa = {
            "titulo": titulo,
            "descricao": descricao,
            "data": data,
            "hora": hora,
            "categoria": categoria
        }

        tarefas[self.usuario_logado].append(nova_tarefa)
        salvar_dados(TASKS_FILE, tarefas)
        messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")

    def listar_tarefas(self):
        tarefas = carregar_dados(TASKS_FILE)
        lista = tarefas.get(self.usuario_logado, [])
        if not lista:
            messagebox.showinfo("Tarefas", "Nenhuma tarefa cadastrada.")
            return

        janela = tk.Toplevel(self.root)
        janela.title("Suas Tarefas")
        for tarefa in lista:
            texto = f"{tarefa['titulo']} - {tarefa['categoria']}\n{tarefa['data']} às {tarefa['hora']}\n{tarefa['descricao']}\n"
            tk.Label(janela, text=texto, justify="left", anchor="w").pack(padx=10, pady=5)

    def excluir_tarefa(self):
        tarefas = carregar_dados(TASKS_FILE)
        lista = tarefas.get(self.usuario_logado, [])
        if not lista:
            messagebox.showinfo("Tarefas", "Nenhuma tarefa para excluir.")
            return

        opcoes = [f"{i+1}. {t['titulo']}" for i, t in enumerate(lista)]
        escolha = simpledialog.askinteger("Excluir", "\n".join(opcoes) + "\n\nDigite o número da tarefa para excluir:")

        if escolha and 1 <= escolha <= len(lista):
            del lista[escolha - 1]
            tarefas[self.usuario_logado] = lista
            salvar_dados(TASKS_FILE, tarefas)
            messagebox.showinfo("Sucesso", "Tarefa excluída.")
        else:
            messagebox.showwarning("Aviso", "Número inválido.")

# Executar o app
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
    app = SistemaTarefas(root)
    root.mainloop()

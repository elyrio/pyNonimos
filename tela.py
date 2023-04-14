#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import Libraries
import pyNonimos

from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os

class Tela():

    def abrirArquivo(self):
        self.filename = filedialog.askopenfilename(title="Selecione um arquivo PDF",
                                                   filetypes=(("PDf",
                                                               "*.pdf*"),
                                                              ))
        try:
            if os.path.isfile(self.filename):
                pyNonimos.extract_info(input_file=self.filename)
                palavras=[]
                linhas = self.texto.get(0.0, tk.END)
                linhas = linhas.split('\n')
                for linha in linhas:
                    if (linha != ''):
                        palavras.append(linha)
                pyNonimos.process_file(input_file=self.filename, search_str=palavras,
                                    pages=None, action='Redact')
                arquivo = os.path.basename(self.filename)
            tk.messagebox.showinfo(title='Anonimização - PMSMJ', message='Arquivo \"'+ arquivo + '\", foi Anonimizado com sucesso!')
        except:
            pass

    def salvarBusca(self):
        with open("configs\/busca.txt", "w", encoding="utf-8") as arquivo:
            text = self.texto.get(0.0, tk.END)
            arquivo.write(text)  # Escreve o texto no arquivo criado
        tk.messagebox.showinfo(title='Arquivo de busca - PMSMJ',
                               message='Arquivo de busca salvo com sucesso!')
    
    def show_about(self):
        tk.messagebox.showinfo(
            title='Sobre - pyNonimos', message='Aplicativo desenvolvido pela Controladoria Interna da Prefeitrua Municipal de Santa Maria de Jetibá - ES. \n \n  A anonimização de PDF é um processo importante para proteger informações sensíveis e garantir a privacidade dos usuários. \n O projeto consiste em uma aplicação desktop que permite aos usuários anonimizar arquivos PDF selecionados. A aplicação é desenvolvida em Python. \n \n Versão : 1.0 - beta \n Desenvolvedor: Ewerton Lyrio Nascimento \n Março de 2023.')
    

    def __init__(self, master):
        self.TelaApp = master
        self.barra_menu = tk.Menu(self.TelaApp)
        
        self.texto = Text(self.TelaApp, font="arial 14")
        arquivoBusca = open("configs\/busca.txt", "r", encoding="utf-8")
        dadosBusca = arquivoBusca.read()
        self.texto.insert(0.0, dadosBusca)

        self.anomizacao_menu = tk.Menu(self.barra_menu, tearoff=0)
        self.anomizacao_menu.add_command(
            label="Selecionar arquivo para anonimizar", command=self.abrirArquivo)
        self.anomizacao_menu.add_command(
            label="Salvar dados de Busca", command=self.salvarBusca)
        self.anomizacao_menu.add_separator()
        self.anomizacao_menu.add_command(
            label="Sair", command=self.TelaApp.quit)
        self.barra_menu.add_cascade(
            label="Anonimização", menu=self.anomizacao_menu)
        
        self.help_menu = tk.Menu(self.barra_menu, tearoff=0)
        self.help_menu.add_command(label="Sobre", command=self.show_about)
        self.barra_menu.add_cascade(label="Ajuda", menu=self.help_menu)
        self.TelaApp.config(menu=self.barra_menu)

        self.texto.pack()

app = tk.Tk()
app.title("PyNonimos - PMSMJ")
app.geometry("800x600")
app.iconbitmap("brasao.ico")
app.minsize(height=600, width=800)
app.maxsize(height=600, width=800)
app.configure(background="#f2f8fb")


Tela(app)
app.mainloop()

from tkinter import *
from tkinter import Tk, ttk, messagebox
from cores import * 

from PIL import Image, ImageTk

#BARA DE PROGRESSO DO TKINTER
from tkinter.ttk import Progressbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure

#Tkcalendar
from tkcalendar import Calendar, DateEntry
from datetime import date

#Import de funcoes da views
from view import *

#Janela vazia

janela = Tk()
janela.title()
janela.geometry('900x650')
janela.configure(background='#e9edf5')
janela.resizable(width=FALSE, height=FALSE) #tamanho da tela não ajustavél 

style = ttk.Style(janela)
style.theme_use("clam")

#Criando frames para dividir a tela do app
frameCima = Frame(janela, width=1043, height=50, bg=co1, relief="flat")
frameCima.grid(row=0, column=0)

frameMeio = Frame(janela, width=1043, height=361, bg=co1, pady=20, relief="raised")
frameMeio.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

frameBaixo = Frame(janela, width=1043, height=300, bg=co1, relief="flat")
frameBaixo.grid(row=2, column=0, pady=0, padx=10, sticky=NSEW)

frame_gra_pie = Frame(frameMeio, width=580, height=250, background=co2)
frame_gra_pie.place(x=415, y=5)

#Frame superior
app_img = Image.open('logo.png')
app_img = app_img.resize((60,60))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text=" ORÇAMENTO DA CASA ", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co4)
app_logo.place(x=0, y=0)

# Definindo tree como global
global tree

#Função inserir no Banco de dados os valores de categoria:
def inserir_categoria_bd():
    nome = e_categoria.get()

    lista_inserir = [nome]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
        
    # Passando lista para função da view:    
    inserir_categoria(lista_inserir)

    messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso!')

    e_categoria.delete(0, 'end')

    # Pegando valores da categoria:
    categorias_funcao = ver_categoria()
    categoria = []

    for i in categorias_funcao:
        categoria.append(i[1])

    #Atualizando a lista de categorias:
    combo_categoria_despesa['values'] = (categoria)
    

#Função inserir no Banco de dados os valores de receitas:
def inserir_receitas_bd():
    nome = 'Receita'
    data = e_cal_receitas.get()
    quantia = e_valor_receitas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
    #Funcao de inserir da view
    inserir_receita(lista_inserir)

    messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso!')
    
    e_cal_receitas.delete(0,'end')
    e_valor_receitas.delete(0, 'end')

    #Atualizando dados 
    mostrar_renda()
    percentual()
    grafico_bar()
    resumo()
    grafico_pie()

#Função inserir no Banco de dados os valores de despesas:
def inserir_depesas_bd():
    nome = combo_categoria_despesa.get()
    data = e_cal_despesa.get()
    quantia = e_valor_despesas.get()

    lista_inserir = [nome, data, quantia]

    for i in lista_inserir:
        if i == '':
            messagebox.showerror('Erro', 'Preencha todos os campos')
            return
    #Funcao de inserir da view
    inserir_gastos(lista_inserir)

    messagebox.showinfo('Sucesso', 'Dados inseridos com sucesso!')
    
    combo_categoria_despesa.delete(0, 'end')
    e_cal_despesa.delete(0,'end')
    e_valor_despesas.delete(0, 'end')

    #Atualizando dados 
    mostrar_renda()
    percentual()
    grafico_bar()
    resumo()
    grafico_pie()

# FUNÇÃO DELETAR DO BANCO DE DADOS:
def deletar_dados():
    try:
        treev_dados = tree.focus()
        treev_dicionario = tree.item(treev_dados)
        treev_lista = treev_dicionario['values']
        valor = treev_lista[0]
        nome = treev_lista[1]

        if nome == 'Receita':
            deletar_receita([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso!')
            
            #Atualizando dados 
            mostrar_renda()
            percentual()
            grafico_bar()
            resumo()
            grafico_pie()

        else:
            deletar_gastos([valor])
            messagebox.showinfo('Sucesso', 'Os dados foram deletados com sucesso!')
            
            #Atualizando dados 
            mostrar_renda()
            percentual()
            grafico_bar()
            resumo()
            grafico_pie()

    except IndexError:
        messagebox.showerror('Erro', 'Selecione um dos dados na tabela')
      


#Percentual 
def percentual():
    l_nome = Label(frameMeio, text='Gasto Mensal', height=1,anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_nome.place(x=7, y=5)

    style = ttk.Style()
    style.theme_use('default')
    style.configure('black.Horizontal.TProgressbar', background= '#daed6b')
    style.configure('TProgressbar', thickness=25)

    bar = Progressbar(frameMeio, length=180, style='black.Horizontal.TProgressbar')
    bar.place(x=10, y=35)
    bar['value'] = percentagem_valor()[0]

    valor = float(percentagem_valor()[0])


    l_percentagem = Label(frameMeio, text='{:,.2f}%'.format(valor),anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_percentagem.place(x=200, y=35)

#Graficos bar 

def grafico_bar():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = bar_valores()

    #Fazer figuras e atribir objetos
    figura = plt.Figure(figsize=(4, 3.45), dpi=60)
    ax = figura.add_subplot(111)

    ax.bar(lista_categorias, lista_valores, color=colors, width=0.9)

    c = 0

    for i in ax.patches:
        # get_x pulls left or right; get_height pushes up or down
        ax.text(i.get_x()-.001, i.get_height()+.5,
                str("{:,.0f}".format(lista_valores[c])), fontsize=17, fontstyle='italic',  verticalalignment='bottom',color='dimgrey')
        c += 1

    ax.set_xticklabels(lista_categorias, fontsize=16) # Set the tick labels

    ax.patch.set_facecolor('#ffffff')
    ax.spines['bottom'].set_color('#CCCCCC')
    ax.spines['bottom'].set_linewidth(1)
    ax.spines['right'].set_linewidth(0)
    ax.spines['top'].set_linewidth(0)
    ax.spines['left'].set_color('#CCCCCC')
    ax.spines['left'].set_linewidth(1)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.tick_params(bottom=False, left=False)
    ax.set_axisbelow(True)
    ax.yaxis.grid(False, color='#EEEEEE')
    ax.xaxis.grid(False)

    canva = FigureCanvasTkAgg(figura, frameMeio)
    canva.get_tk_widget().place(x=10, y=70)

# Função de resumo total

def resumo():
    valor = bar_valores()

# PRIMEIRO FRAME DE VALOR DE CIMA 
    l_linha = Label(frameMeio, text='', width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=52)
    l_sumario = Label(frameMeio, text='TOTAL RENDA MENSAL      ', anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=35)
    l_sumario = Label(frameMeio, text='R$ {:,.2f}'.format(valor[0]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=70)

# SEGUNDO FRAME DE VALOR 
    l_linha = Label(frameMeio, text='', width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=132)
    l_sumario = Label(frameMeio, text='TOTAL DEPESA MENSAL      ', anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=115)
    l_sumario = Label(frameMeio, text='R$ {:,.2f}'.format(valor[1]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=150)

# TERCEITO FRAME DE VALOR   
    l_linha = Label(frameMeio, text='', width=215, height=1, anchor=NW, font=('Arial 1'), bg='#545454')
    l_linha.place(x=309, y=207)
    l_sumario = Label(frameMeio, text='SALDO TOTAL CONTA      ', anchor=NW, font=('Verdana 12'), bg=co1, fg='#83a9e6')
    l_sumario.place(x=309, y=190)
    l_sumario = Label(frameMeio, text='R$ {:,.2f}'.format(valor[2]), anchor=NW, font=('Arial 17'), bg=co1, fg='#545454')
    l_sumario.place(x=309, y=220)

# funcao grafico pie
def grafico_pie():
    # faça figura e atribua objetos de eixo
    figura = plt.Figure(figsize=(5, 3), dpi=90)
    ax = figura.add_subplot(111)

    lista_valores = pie_valores()[1]
    lista_categorias = pie_valores()[0]

    # only "explode" the 2nd slice (i.e. 'Hogs')

    explode = []
    for i in lista_categorias:
        explode.append(0.05)

    ax.pie(lista_valores, explode=explode, wedgeprops=dict(width=0.2), autopct='%1.1f%%', colors=colors,shadow=True, startangle=90)
    ax.legend(lista_categorias, loc="center right", bbox_to_anchor=(1.55, 0.50))

    canva_categoria = FigureCanvasTkAgg(figura, frame_gra_pie)
    canva_categoria.get_tk_widget().grid(row=0, column=0)



percentual()
grafico_bar()
resumo()
grafico_pie()


#Criando frames dentro do FRAME BAIXO
frame_renda = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_renda.grid(row=0, column=0)

frame_operacoes = Frame(frameBaixo, width=220, height=250, bg=co1)
frame_operacoes.grid(row=0, column=1,padx=5)

frame_configuracao = Frame(frameBaixo, width=300, height=250, bg=co1)
frame_configuracao.grid(row=0, column=2, padx=5)


#TABELA RENDA MENSAL:
app_tabela = Label(frameMeio, text=" TABELA DE RECEITAS DE DESPESAS ", anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
app_tabela.place(x=5, y=309)

#FUNCAO QUE MOSTRA TABELA
def mostrar_renda():

    # creating a treeview with dual scrollbars
    tabela_head = ['#Id','Categoria','Data','Quantidade']

    lista_itens = tabela()
    global tree

    tree = ttk.Treeview(frame_renda, selectmode="extended",columns=tabela_head, show="headings")
    # vertical scrollbar
    vsb = ttk.Scrollbar(frame_renda, orient="vertical", command=tree.yview)
    # horizontal scrollbar
    hsb = ttk.Scrollbar(frame_renda, orient="horizontal", command=tree.xview)

    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(column=0, row=0, sticky='nsew')
    vsb.grid(column=1, row=0, sticky='ns')
    hsb.grid(column=0, row=1, sticky='ew')

    hd=["center","center","center", "center"]
    h=[30,100,100,100]
    n=0

    for col in tabela_head:
        tree.heading(col, text=col.title(), anchor=CENTER)
        # adjust the column's width to the header string
        tree.column(col, width=h[n],anchor=hd[n])
        
        n+=1

    for item in lista_itens:
        tree.insert('', 'end', values=item)


mostrar_renda()
#Despesa
l_info = Label(frame_operacoes, text='Insira novas Despesas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

#Categoria
l_categoria = Label(frame_operacoes, text='Categoria', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10, y=40)

categoria_funcao = ver_categoria()
categoria = []

for i in categoria_funcao:
    categoria.append(i[1])

combo_categoria_despesa = ttk.Combobox(frame_operacoes, width=10, font=('Ivy 10'))
combo_categoria_despesa['values'] = (categoria)
combo_categoria_despesa.place(x=110, y=41)

# Data 
l_cal_despesas = Label(frame_operacoes, text='Data', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_despesas.place(x=10, y=70)
e_cal_despesa = DateEntry(frame_operacoes, width=12, background= 'darkblue', foreground='white', borderwidth=2, year=2023)
e_cal_despesa.place(x=110, y=71)

# Adicona valor 
l_valor_despesas = Label(frame_operacoes, text='Quantia Total', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_despesas.place(x=10, y=100)
e_valor_despesas = Entry(frame_operacoes, width=14, justify='left', relief='solid')
e_valor_despesas.place(x=110, y=101)

#Botão inserir 
img_add_despesas = Image.open('images.png')
img_add_despesas = img_add_despesas.resize((17,17))
img_add_despesas = ImageTk.PhotoImage(img_add_despesas)
botao_inserir_despesas = Button(frame_operacoes, image=img_add_despesas, text="Adicionar:",command=inserir_depesas_bd, width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_despesas.place(x=110, y=131)

#Botão excluir
l_excluir_categoria = Label(frame_operacoes, text='Excluir ação:', height=1, anchor=NW, font=('Ivy 10 bold'), bg=co1, fg=co4)
l_excluir_categoria.place(x=10, y=190)
img_delete = Image.open('delete.png')
img_delete = img_delete.resize((17,17))
img_delete = ImageTk.PhotoImage(img_delete)
botao_deletar = Button(frame_operacoes,command=deletar_dados, image=img_delete, text="Deletar:", width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_deletar.place(x=110, y=190)


#Configurando Receitas

l_info = Label(frame_configuracao, text='Insira novas Receitas', height=1, anchor=NW, font=('Verdana 10 bold'), bg=co1, fg=co4)
l_info.place(x=10, y=10)

#Calendario ---------------
l_cal_receitas = Label(frame_configuracao, text='Data:', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_cal_receitas.place(x=10, y=40)
e_cal_receitas = DateEntry(frame_configuracao, width=12, background= 'darkblue', foreground='white', borderwidth=2, year=2022)
e_cal_receitas.place(x=110, y=41)


#Para inserir valor ----------
l_valor_receitas = Label(frame_configuracao, text='Quantia Total:', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_valor_receitas.place(x=10, y=70)
e_valor_receitas = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_valor_receitas.place(x=110, y=71)

#Botao de adicionar receitas
img_add_receitas = Image.open('images.png')
img_add_receitas = img_add_receitas.resize((17,17))
img_add_receitas = ImageTk.PhotoImage(img_add_receitas)
botao_inserir_receitas = Button(frame_configuracao, image=img_add_receitas, text="Adicionar",command=inserir_receitas_bd, width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_receitas.place(x=110, y=111)

#Adicionando categoria novas ---------
l_categoria = Label(frame_configuracao, text='Categoria:', height=1, anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
l_categoria.place(x=10, y=160)
e_categoria = Entry(frame_configuracao, width=14, justify='left', relief='solid')
e_categoria.place(x=110, y=161)
#Botao de adicionar categoria ------------
img_add_categoria = Image.open('images.png')
img_add_categoria = img_add_categoria.resize((17,17))
img_add_categoria = ImageTk.PhotoImage(img_add_categoria)
botao_inserir_categoria = Button(frame_configuracao,command=inserir_categoria_bd, image=img_add_categoria, text="Adicionar", width=80, compound=LEFT, anchor=NW, font=('Ivy 7 bold'), bg=co1, fg=co0, overrelief=RIDGE)
botao_inserir_categoria.place(x=110, y=190)



janela.mainloop()



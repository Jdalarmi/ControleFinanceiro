from tkinter import *
from tkinter import Tk, ttk
from cores import * 

from PIL import Image, ImageTk

#BARA DE PROGRESSO DO TKINTER
from tkinter.ttk import Progressbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure


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

#Frame superior
app_img = Image.open('logo.png')
app_img = app_img.resize((60,60))
app_img = ImageTk.PhotoImage(app_img)

app_logo = Label(frameCima, image=app_img, text=" ORÇAMENTO DA CASA ", width=900, compound=LEFT, padx=5, relief=RAISED, anchor=NW, font=('Verdana 20 bold'), bg=co1, fg=co4)
app_logo.place(x=0, y=0)

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
    bar['value'] = 50

    valor = 50

    l_percentagem = Label(frameMeio, text='{:,.2f}%'.format(valor),anchor=NW, font=('Verdana 12'), bg=co1, fg=co4)
    l_percentagem.place(x=200, y=35)


#Graficos bar 

def grafico_bar():
    lista_categorias = ['Renda', 'Despesas', 'Saldo']
    lista_valores = [3000, 2000, 6320]

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

    ax.set_xticklabels(lista_categorias,fontsize=16)

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


percentual()
grafico_bar()

janela.mainloop()


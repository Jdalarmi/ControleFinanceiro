import sqlite3 as lite
import pandas as pd

con = lite.connect('dados.db')
#Funcoes de inserção
# Inserir categoria
def inserir_categoria(i):
    
    with con:
        cur = con.cursor()
        query = "INSERT INTO Categoria (nome) VALUES (?)"
        cur.execute(query,i) 
# Inserir receita
def inserir_receita(i):
    
    with con:
        cur = con.cursor()
        query = "INSERT INTO Receitas (categoria, adicinado_em, valor) VALUES (?,?,?)"
        cur.execute(query, i) 
# Inserir gastos
def inserir_gastos(i):
    
    with con:
        cur = con.cursor()
        query = "INSERT INTO Gastos (categoria, retirado_em,valor) VALUES (?,?,?)"
        cur.execute(query,i) 

#Funcoes para deletar
def deletar_receita(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Receitas WHERE id=?"
        cur.execute(query, i)

def deletar_gastos(i):
    with con:
        cur = con.cursor()
        query = "DELETE FROM Gastos WHERE id=?"
        cur.execute(query, i)

# Funções para ver dados


def ver_categoria():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Categoria")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

def ver_receitas():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Receitas")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

def ver_gastos():
    lista_itens = []
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM Gastos")
        linha = cur.fetchall()
        for l in linha:
            lista_itens.append(l)
    return lista_itens

def tabela():
    gastos = ver_gastos()
    receitas = ver_receitas()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    for i in receitas:
        tabela_lista.append(i)

    return tabela_lista


def bar_valores():

    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)


    #Receita total
    receitas = ver_gastos()
    despesa_lista = []

    for i in receitas:
        despesa_lista.append(i[3])

    despesas_total = sum(despesa_lista)

    #Despesa total
    saldo_total = receita_total - despesas_total

        
    return [receita_total, despesas_total, saldo_total]

def pie_valores():
    gastos = ver_gastos()

    tabela_lista = []

    for i in gastos:
        tabela_lista.append(i)

    dataframe = pd.DataFrame(tabela_lista, columns=['id', 'categoria', 'Data', 'valor' ])
    dataframe = dataframe.groupby('categoria')['valor'].sum()

    lista_quantias = dataframe.values.tolist()
    lista_categoria = []

    for i in dataframe.index:
        lista_categoria.append(i)

    return ([lista_categoria, lista_quantias])

#Percentual da barra 
def percentagem_valor():
    receitas = ver_receitas()
    receitas_lista = []

    for i in receitas:
        receitas_lista.append(i[3])

    receita_total = sum(receitas_lista)


    #Receita total
    receitas = ver_gastos()
    despesa_lista = []

    for i in receitas:
        despesa_lista.append(i[3])

    despesas_total = sum(despesa_lista)

    # % total 
    total = ((receita_total - despesas_total) / receita_total) * 100

    return [total]
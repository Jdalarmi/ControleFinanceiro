import sqlite3 as lite

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

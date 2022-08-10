import streamlit as st
import datetime
import win32print
import win32api
import sqlite3
import time
import threading
import pymysql
# import win32print
# import win32api
import os


data = datetime.datetime.now()
data_str = data.strftime("%d/%m/%y")
hora = datetime.datetime.now()
hora_str = hora.strftime("%H:%M:%S")
data_hora = data.strftime("%y/%m/%d") + " " +hora_str

conexao = pymysql.connect(host='DESKTOP-IDQTBUT',user='root', database='banco_dados', password='pindoba10')


id_produto = []


st.set_page_config(page_title='Comanda', page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)
page = ['Vender','Lista de Comandas','Movimentação']
st.sidebar.image('img.png')
pagina_atual = st.sidebar.radio('',page)


st.title('Comanda Pré-Paga')

if pagina_atual == 'Vender':
    

    st.header('Venda')
    n_comanda = st.text_input(label='Numero da comanda')
    
    # ler  = st.button(label='Ler Comanda')
    
    if n_comanda:
        try:
            # if n_comanda != "" :
                banco = conexao.cursor()
                cursor = conexao.cursor()
                cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+n_comanda+"'")
                dados_comanda = cursor.fetchall()
                valor = dados_comanda[0][0]
                nome = dados_comanda[0][1]

                st.text('Comanda: '+n_comanda)
                st.text('\nNome: '+nome)
                st.text('\nValor: R$ '+ str(valor))
                
                with st.form(key='myform', clear_on_submit=True):
                    codigo_produto = st.text_input(label='Produto')
                    vender = st.form_submit_button('vender')
                    
                if codigo_produto:
                    
                    banco = conexao.cursor()
                    cursor = conexao.cursor()
                    cursor.execute("SELECT nome, valor, imprimir FROM produtos WHERE codigo_produto = '"+codigo_produto+"'")
                    dados_produto = cursor.fetchall()
                    produto = dados_produto[0][0]
                    preco = dados_produto[0][1]
                    imprimir = dados_produto[0][2]
                    saldo_final = dados_comanda[0][0] - preco

                    if saldo_final < 0:
                        st.info('Saldo insuficiente!')
                    else:
                        if imprimir == True:
                            cursor = conexao.cursor()
                            cursor.execute("SELECT nome FROM produtos WHERE codigo_produto = '"+str(codigo_produto)+"'")
                            dados_comanda = cursor.fetchall()

                            arquivo = open("print.txt", "w")
                            arquivo.write("Comanda: "+n_comanda)
                            arquivo.write("\n\n"+produto+"\n\n")
                            arquivo.write(nome+"\n\n")
                            arquivo.write("HORA: "+hora_str)
                            arquivo.write("\nDATA: "+ data_str)
                            arquivo.write("\n          ...")
                            arquivo.close()

                            lista_impressoras = win32print.EnumPrinters(2)
                            impressora = lista_impressoras[4]
                            win32print.SetDefaultPrinter(impressora[2])
                            win32api.ShellExecute(0, "print", "print.txt", None, ".", 0)
                            st.info(produto+' foi debitado da comanda '+n_comanda)
                            st.info('Novo saldo: R$ '+str(saldo_final))
                            time.sleep(0.7)
                            cursor.execute("INSERT INTO historicos (evento, numero_comanda, nome, produto, valor, data) VALUES ('{}', '{}', '{}','{}', {}, '{}')".format("VENDA",n_comanda,nome, produto,preco, data_hora))
                            cursor.execute("commit;")
                        else:

                            cursor.execute(f"UPDATE comandas SET valor = '{saldo_final:.2f}' WHERE numero_comanda = {n_comanda}")
                            cursor.execute("commit;")
                            banco.close()
                            st.info(produto+' foi debitado da comanda '+n_comanda)
                            st.info('Novo saldo: R$ '+str(saldo_final))
                        
  

        except:
            # st.table('dddd')
            st.info('Produto nao encontrado')

    # elif

elif pagina_atual == 'Lista de Comandas':
    st.header("Lista das Comandas")
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM comandas")
    dados_lidos = cursor.fetchall()
    st.table(dados_lidos)

elif pagina_atual =='Movimentação':
    st.header('Movimentação')
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM historicos")
    dados_lidos = cursor.fetchall()

    st.table(dados_lidos)

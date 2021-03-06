import datetime
from PyQt5 import uic, QtWidgets
import sqlite3
import time
import threading
import pymysql
import win32print
import win32api
import os
import bcrypt
import util


data = datetime.datetime.now()
data_str = data.strftime("%d/%m/%y")
hora = datetime.datetime.now()
hora_str = hora.strftime("%H:%M:%S")
data_hora = data_str + " " +hora_str


conexao = pymysql.connect(host='DESKTOP-IDQTBUT',user='root', database='banco_dados', password='pindoba10')

# senha = util.criar_senha('123456')
# print(senha)
# entrar = str(input('Digite a senha certa:\n'))
# senhadb = '123456'
# login_ok = util.verificar_senha(entrar,senha)


lista_preco = []
lista_produto = []
id_produto = []

def iniciar():

    # nome = 'RAUL ROCK BAR'
    # banco = sqlite3.connect('banco_dados.db')
    # cursor = banco.cursor()
    # cursor.execute(
    #     "CREATE TABLE IF NOT EXISTS comandas (id INTEGER PRIMARY KEY AUTOINCREMENT, numero integer, valor REAL, nome text)")
    # cursor.execute("CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, codigo integer, nome text, valor REAL )")
    # banco.commit()
    # banco.close()
    
    listar_dados()
    historico()

def criar_user():
    
    nome = user.lineEdit.text()
    senha = user.lineEdit_2.text()
    nivel = user.lineEdit_3.text()

def salvar_user():
    nome =  user.lineEdit.text()
    entrada_senha = str(util.criar_senha(user.lineEdit_2.text())).replace("'","")
    senha = entrada_senha[1:]
    nivel = user.lineEdit_3.text()
    print(str(senha))
    print(type(senha))

    banco = conexao.cursor()
    cursor = conexao.cursor()
    # cursor.execute(f"INSERT INTO banco_dados.users VALUES (1,'{nome}'), (2,'{senha}'), (3,'{nivel}')")
    cursor.execute("INSERT INTO users (nome, senha, nivel) VALUES ('{}', '{}', '{}')".format(nome,senha,nivel))

    # cursor.execute(f"INSERT INTO banco_dados.users (nome, senha, nivel) VALUES ('{nome}', {senha}, '{nivel}')")
    cursor.execute("commit;")
    banco.close()

    user.label.setText("Usuário Cadastrado com sucesso!")
    
def add_produto():
    global lista_preco
    global lista_produto
    numero_comanda = forme.lineEdit_3.text()

    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT valor FROM comandas WHERE numero_comanda ={numero_comanda}")
    dados_comanda = cursor.fetchall()
    valor_atual = dados_comanda[0][0]   
    numero_produto = add.lineEdit.text()
    if int(numero_produto) > 1000 and int(numero_produto) < 2000:
        id_produto.append(int(numero_produto))
    else:
        pass
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT nome, valor FROM produtos WHERE codigo_produto = {numero_produto}")
    dados_produto = cursor.fetchall()
    # print(lista_produto)
    # print(dados_produto[0][0])
    lista_produto.append(dados_produto[0][0])
    lista_preco.append(dados_produto[0][1])
    add.listWidget.addItem(dados_produto[0][0])
    add.listWidget_2.addItem("R$ "+str(dados_produto[0][1]))
    # print(dados_produto[0][1])
    # add.label_9.setText(str(dados_produto[0][0]))
    # nome = forme.lineEdit_3.text()
    
    subtotal = sum(lista_preco)
    novo_valor = valor_atual - subtotal
    add.label_7.setText(" R$ "+str(novo_valor))
    add.label_5.setText(" R$ "+str(subtotal))
    add.lineEdit.setText("")
    if novo_valor < 0:
        ero.show()

    # if valor == '':
    #     forme.lineEdit.setText('')
    # else:

    #     try:
    #         banco = sqlite3.connect('banco_dados.db')
    #         cursor = banco.cursor()
    #         cursor.execute("INSERT INTO dados (nome, status) VALUES ('" + nome + "', '" + status + "')")
    #         banco.commit()
    #         banco.close()
    #         print('dados inseridos com sucesso')

    #     except sqlite3.Error as erro:
    #         print("deu erro", erro)
    #         print(nome, status)


    # listar_dados()
    # forme.lineEdit.setText("")
def entrar_guarida():
    nome = forme.lineEdit_5.text()
    senha = forme.lineEdit_6.text()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT senha, nome FROM users WHERE nome = '{nome}'")
    dados_user = cursor.fetchall()
    print(dados_user[0][0])

    senha_verificada = util.verificar_senha(senha, dados_user[0][0])
    print(senha_verificada)


    if nome == dados_user[0][1] and senha_verificada == True:
        forme.label.setText("")
        guarida.show()

    else:
        forme.label.setText("Usuário ou Senha incorreto")

def alterar_nome():
    numero_comanda = forme.lineEdit_8.text()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute(f"SELECT nome FROM comandas WHERE numero_comanda = {numero_comanda}")
    dados_comanda = cursor.fetchall()
    # valor_atual = dados_comanda[0][0]
    # nome_db = dados_comanda[0][0]
    nome = forme.lineEdit_7.text()       
        
    if nome != "":
    
        banco = conexao.cursor()
        cursor = conexao.cursor()
        cursor.execute(f"UPDATE comandas SET nome = '{nome}' WHERE numero_comanda = {numero_comanda}")
        cursor.execute("commit;")
        banco.close()
        forme.label_4.setText("Nome alterado com sucesso!")
        forme.lineEdit_7.setText("")
        forme.lineEdit_8.setText("")
        listar_dados()
        
    else:
        forme.label_4.setText("Nenhum nome foi digitado!")
        forme.lineEdit_7.setText("")
        forme.lineEdit_8.setText("")
        
def add_saldo():
    if guarida.lineEdit.text() != "" and guarida.lineEdit_2.text() != "":
        
        banco = conexao.cursor()
        cursor = conexao.cursor()
        cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+guarida.lineEdit.text()+"'")
        dados_comanda = cursor.fetchall()
        valor_atual = dados_comanda[0][0]
        nome_db = dados_comanda[0][1]
        nome = guarida.lineEdit_4.text()
        valor_inserir = float(guarida.lineEdit_2.text())
        valor_atualizado = valor_atual + valor_inserir
        numero_comanda = guarida.lineEdit.text()

        if nome != "":

            banco = conexao.cursor()
            cursor = conexao.cursor()
            cursor.execute(f"UPDATE comandas SET nome = '{nome}', valor = '{valor_atualizado:.2f}' WHERE numero_comanda = {numero_comanda}")
            cursor.execute("INSERT INTO historicos (evento, numero_comanda, nome, produto, valor, data) VALUES ('{}', '{}', '{}','{}', {}, '{}')".format("ENTRADA",guarida.lineEdit.text(),nome,"CREDITO",valor_inserir, data_hora))
            cursor.execute("commit;")
            banco.close()
            historico()

        else:
            banco = conexao.cursor()
            cursor = conexao.cursor()
            cursor.execute(f"UPDATE comandas SET nome = '{nome_db}', valor = '{valor_atualizado:.2f}' WHERE numero_comanda = {numero_comanda}")
            cursor.execute("INSERT INTO historicos (evento, numero_comanda, nome, produto, valor, data) VALUES ('{}', '{}', '{}','{}', {}, '{}')".format("ENTRADA",guarida.lineEdit.text(),nome_db,"CREDITO",valor_inserir, data_hora))           
            cursor.execute("commit;")
            banco.close()
            historico()
            

        guarida.label.setText("")
        guarida.label_3.setText("")
        guarida.label_2.setText("")
        guarida.lineEdit.setText("")
        guarida.lineEdit_2.setText("")
        guarida.lineEdit_4.setText("")
        status = f"Comanda {numero_comanda} agora tem R$ {valor_atualizado:.2f} de saldo!"
        guarida.label_4.setText(status)
        listar_dados()

def ler():
    if guarida.lineEdit.text() != "" or guarida.lineEdit_2.text() != "":
        banco = conexao.cursor()
        cursor = conexao.cursor()
        cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+guarida.lineEdit.text()+"'")
        dados_comanda = cursor.fetchall()
        valor = dados_comanda[0][0]
        nome = dados_comanda[0][1]
        guarida.label.setText(guarida.lineEdit.text())
        guarida.label_3.setText(nome)
        guarida.label_2.setText("R$ "+str(valor))

def janela_comanda():
    add.show()
    lista_preco.clear()
    lista_produto.clear()
    add.label_5.setText("R$ 0.00")
    add.label_7.setText("R$ 0.00")
    # forme.lineEdit_3.setText("")
    add.listWidget.clear()
    add.listWidget_2.clear()
    
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+forme.lineEdit_3.text()+"'")
    dados_comanda = cursor.fetchall()
    valor_atual = dados_comanda[0][0]
    add.label_6.setText("R$ "+str(dados_comanda[0][0]))
    add.label_10.setText(dados_comanda[0][1])
    add.label.setText("N°: "+forme.lineEdit_3.text())

def confirmar_pedido():
    if add.lineEdit.text() != "":
        global lista_preco
    global lista_produto
    numero_comanda = forme.lineEdit_3.text()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT valor FROM comandas WHERE numero_comanda = '"+numero_comanda+"'")
    dados_comanda = cursor.fetchall()
    valor_atual = dados_comanda[0][0]
    soma = sum(lista_preco)  
    saldo_final = valor_atual - soma

    

    cursor2 = conexao.cursor()
    cursor2.execute("SELECT nome FROM comandas WHERE numero_comanda = '"+numero_comanda+"'")
    nome_comanda = cursor2.fetchall()
    print(id_produto)
    n = 0
    for i in id_produto:
        
        # if id_produto[n] > 1000 and id_produto[n] < 2000:
            
            # for j in range(len(id_produto)):
                cursor = conexao.cursor()
                cursor.execute("SELECT nome FROM produtos WHERE codigo_produto = '"+str(id_produto[n])+"'")
                dados_comanda = cursor.fetchall()

                print(n)
                arquivo = open("print.txt", "w")
                # arquivo.write(str(n))
                arquivo.write("Comanda: "+numero_comanda)
                arquivo.write("\n\n"+dados_comanda[0][0]+"\n\n")
                arquivo.write("\n"+nome_comanda[0][0]+"\n\n")
                arquivo.write("HORA: "+hora_str)
                arquivo.write("\nDATA: "+ data_str)
                arquivo.write("\n          ...")
                arquivo.close()

                lista_impressoras = win32print.EnumPrinters(2)
                impressora = lista_impressoras[4]
                win32print.SetDefaultPrinter(impressora[2])
                win32api.ShellExecute(0, "print", "print.txt", None, ".", 0)
                n = n+1        
                time.sleep(0.4)
    indice = 0
    for i in lista_preco:
        cursor.execute("INSERT INTO historicos (evento, numero_comanda, nome, produto, valor, data) VALUES ('{}', '{}', '{}','{}', {}, '{}')".format("VENDA",forme.lineEdit_3.text(),add.label_10.text(), lista_produto[indice],lista_preco[indice], data_hora))
        indice +=1
    historico()

    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute(f"UPDATE comandas SET valor = '{saldo_final:.2f}' WHERE numero_comanda = {numero_comanda}")
    cursor.execute("commit;")
    banco.close()
    add.label_5.setText("R$ 0.00")
    add.label_7.setText("R$ 0.00")
    lista_preco.clear()
    lista_produto.clear()
    id_produto.clear()
    add.listWidget.clear()
    add.listWidget_2.clear()
    forme.lineEdit_3.setText("")
    add.close()
    listar_dados()

def cancelar():
    lista_preco.clear()
    lista_produto.clear()
    add.label_5.setText("R$ 0.00")
    add.label_7.setText("R$ 0.00")
    forme.lineEdit_3.setText("")
    add.listWidget.clear()
    add.listWidget_2.clear()
    add.close()

def zerar():
    valor = "0"
    numero_comanda = guarida.lineEdit.text()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("UPDATE comandas SET valor = '{}', nome = '' WHERE numero_comanda = {}".format(valor, numero_comanda))
    cursor.execute("commit;")
    banco.close()
    
    guarida.label_4.setText("Comanda "+numero_comanda+" foi zerada com sucesso!")
    guarida.label.setText("")
    guarida.label_3.setText("")
    guarida.label_2.setText("")
    guarida.lineEdit.setText("")
    guarida.lineEdit_2.setText("")
    guarida.lineEdit_4.setText("")
    listar_dados()

def erro():
    ero.close()
    cancelar()

def open_user():
    user.show()

def listar_dados():
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM comandas")
    dados_lidos = cursor.fetchall()
    forme.tableWidget.setRowCount(len(dados_lidos))
    forme.tableWidget.setColumnCount(3)
    banco.close()
    print(dados_lidos)
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 3):
            forme.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            
    
    for i in range(0, len(dados_lidos)):
        for j in range(1, 2):
            forme.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem('R$  '+str(dados_lidos[i][j])))
   
def historico():
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM historicos")
    dados_lidos = cursor.fetchall()
    forme.tableWidget_3.setRowCount(len(dados_lidos))
    forme.tableWidget_3.setColumnCount(6)
    banco.close()
    print(dados_lidos)
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            forme.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            

# def excluir():
#     linha = forme.tableWidget.currentRow()
#     forme.tableWidget.removeRow(linha)
#     banco = sqlite3.connect('banco_dados.db')

#     cursor = banco.cursor()
#     cursor.execute("SELECT id FROM dados")
#     dados_lidos = cursor.fetchall()
#     valor_id = dados_lidos[linha][0]
#     cursor.execute("DELETE FROM dados WHERE id=" + str(valor_id))
#     banco.commit()
#     banco.close()
#     listar_dados()


# def editar():
#     linha = forme.tableWidget.currentRow()
#     global numero_id
#     banco = sqlite3.connect('banco_dados.db')
#     cursor = banco.cursor()
    # cursor.execute("SELECT id FROM dados")
    # dados_lidos = cursor.fetchall()
    # valor_id = dados_lidos[linha][0]
    # cursor.execute("SELECT * FROM dados WHERE id=" + str(valor_id))
    # status = cursor.fetchall()
    # numero_id = valor_id
    
    # editor.show()
    # editor.lineEdit.setText(str(status[0][0]))
    # editor.lineEdit_2.setText(str(status[0][1]))
    # editor.lineEdit_3.setText(str(status[0][2]))


# def cantou():
#     banco = sqlite3.connect('banco_dados.db')
#     linha = forme.tableWidget.currentRow()
#     cursor = banco.cursor()
#     cursor.execute("SELECT id FROM dados")
#     dados_lidos = cursor.fetchall()
#     valor_id = dados_lidos[linha][0]

#     cursor.execute("SELECT id FROM dados")
#     valor_id = dados_lidos[linha][0]
#     cursor.execute("SELECT * FROM dados WHERE id=" + str(valor_id))
#     status = cursor.fetchall()
#     banco.close()


#     linha = forme.tableWidget.currentRow()
#     global numero_id
#     banco = sqlite3.connect('banco_dados.db')
#     cursor = banco.cursor()
#     cursor.execute("SELECT id FROM dados")
#     dados_lidos = cursor.fetchall()
#     valor_id = dados_lidos[linha][0]
#     cursor.execute("SELECT * FROM dados WHERE id=" + str(valor_id))
#     status = cursor.fetchall()
#     nome = status[0][1]
#     status_2 = status[0][2]
#     data = datetime.datetime.now()
#     data_str = data.strftime("%d/%m/%y")
#     hora = datetime.datetime.now()
#     hora_str = hora.strftime("%H:%M")
#     cursor.execute("UPDATE dados SET status = 'Cantou' WHERE id = " + str(valor_id))
#     cursor.execute("CREATE TABLE IF NOT EXISTS cantou (id INTEGER PRIMARY KEY AUTOINCREMENT, nome text, status text, data text, hora text)")
#     cursor.execute("INSERT INTO cantou (nome, status, data, hora) VALUES ('" + nome + "', '" + status_2 + "', '" + data_str + "', '" + hora_str + "')")
#     cursor.execute("DELETE FROM dados WHERE id=" + str(valor_id))
#     banco.commit()
#     forme.tableWidget.removeRow(linha)
#     listar_dados()
#     banco.close()


# def salvar():
    # global numero_id
    # nome = editor.lineEdit_2.text()
    # status = editor.lineEdit_3.text()
    # banco = sqlite3.connect('banco_dados.db')
    # cursor = banco.cursor()
    # cursor.execute("UPDATE dados SET nome = '{}', status = '{}' WHERE id = {}".format(nome, status, numero_id))
    # banco.commit()

    # listar_dados()
    # banco.close()
    # editor.close()


# def hora_atualiza():
#     global stop
    
#     for i in range(99999):
#         if stop == True:
#             break
#         hora = datetime.datetime.now()
#         hora_str = hora.strftime("%H:%M")
#         forme.label_4.setText(hora_str)
#         # print(hora_str)
#         time.sleep(59)


# def histo():
    # historico.show()
    # banco = sqlite3.connect('banco_dados.db')
    # cursor = banco.cursor()
    # cursor.execute("SELECT * FROM cantou")
    # # cursor.execute("SELECT * FROM dados WHERE status = ''")
    # dados_lidos = cursor.fetchall()
    # historico.tableWidget.setRowCount(len(dados_lidos))
    # historico.tableWidget.setColumnCount(5)
    # linha = forme.tableWidget.currentRow()

    # banco.close()

    # for i in range(0, len(dados_lidos)):
    #     for j in range(0, 5):
    #         historico.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))


app = QtWidgets.QApplication([])
forme = uic.loadUi("comanda.ui")
add = uic.loadUi("add.ui")
ero = uic.loadUi("erro.ui")
user = uic.loadUi("user.ui")
guarida = uic.loadUi("guarida.ui")
# historico = uic.loadUi("historico.ui")
forme.show()

iniciar()
# threading.Thread(target=hora_atualiza).start()

add.pushButton.clicked.connect(add_produto)
guarida.pushButton_7.clicked.connect(zerar)
forme.pushButton_6.clicked.connect(open_user)
add.pushButton_3.clicked.connect(cancelar)
forme.pushButton_2.clicked.connect(janela_comanda)
add.pushButton_2.clicked.connect(confirmar_pedido)
forme.pushButton_4.clicked.connect(entrar_guarida)
guarida.pushButton.clicked.connect(add_saldo)
guarida.pushButton_3.clicked.connect(ler)
ero.pushButton.clicked.connect(erro)
forme.pushButton_5.clicked.connect(alterar_nome)
user.pushButton.clicked.connect(salvar_user)


app.exec_()


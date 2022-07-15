import datetime
from PyQt5 import uic, QtWidgets
import sqlite3
import time
import threading
import pymysql

conexao = pymysql.connect(host='DESKTOP-IDQTBUT',user='root', database='banco_dados', password='pindoba10')



numero_id = 0

lista_preco = []
lista_produto = []

def iniciar():
    # data = datetime.datetime.now()
    # data_str = data.strftime("%d/%m/%y")
    # nome = 'RAUL ROCK BAR'
    # banco = sqlite3.connect('banco_dados.db')
    # cursor = banco.cursor()
    # cursor.execute(
    #     "CREATE TABLE IF NOT EXISTS comandas (id INTEGER PRIMARY KEY AUTOINCREMENT, numero integer, valor REAL, nome text)")
    # cursor.execute("CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, codigo integer, nome text, valor REAL )")
    # banco.commit()
    # banco.close()
    listar_dados()


def add_produto():
    global lista_preco
    global lista_produto
    # numero_comanda = int(forme.lineEdit_3.text())

    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT valor FROM comandas WHERE numero_comanda = '"+forme.lineEdit_3.text()+"'")
    dados_comanda = cursor.fetchall()
    valor_atual = dados_comanda[0][0]
    # codigo_produto = add.lineEdit.text()
    # add.label_6.setText("R$ "+str(dados_comanda[0][0]))
    # print(dados_comanda[0][0])

    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, valor FROM produtos WHERE codigo = '"+add.lineEdit.text()+"'")
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


def add_saldo():
    if forme.lineEdit.text() != "" and forme.lineEdit_2.text() != "":
        

        banco = conexao.cursor()
        cursor = conexao.cursor()
        cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+forme.lineEdit.text()+"'")
        dados_comanda = cursor.fetchall()
        valor_atual = dados_comanda[0][0]
        nome_db = dados_comanda[0][1]
        print(valor_atual)
        print(nome_db)

        nome = forme.lineEdit_4.text()
        valor_inserir = float(forme.lineEdit_2.text())
        valor_atualizado = valor_atual + valor_inserir
        numero_comanda = forme.lineEdit.text()

        if nome != "":

            banco = sqlite3.connect('banco_dados.db')
            cursor = banco.cursor()
            cursor.execute(f"UPDATE comandas SET nome = '{nome}', valor = '{valor_atualizado:.2f}' WHERE numero_comanda = {numero_comanda}")
            # cursor.execute("UPDATE comandas SET nome = '{}', valor = '{}' WHERE numero = {}".format(nome, valor_atualizado, numero))

            banco.commit()

        else:
            banco = conexao.cursor()
            cursor = conexao.cursor()
            cursor.execute(f"UPDATE comandas SET nome = '{nome_db}', valor = '{valor_atualizado:.2f}' WHERE numero_comanda = {numero_comanda}")
            # banco.commit()
            banco.close()
            

        forme.label.setText("")
        forme.label_3.setText("")
        forme.label_2.setText("")
        forme.lineEdit.setText("")
        forme.lineEdit_2.setText("")
        forme.lineEdit_4.setText("")
        status = f"Comanda {numero_comanda} agora tem R$ {valor_atualizado:.2f} de saldo!"
        forme.label_4.setText(status)
        listar_dados()


def ler():
    if forme.lineEdit.text() != "" or forme.lineEdit_2.text() != "":
        banco = conexao.cursor()
        cursor = conexao.cursor()
        cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+forme.lineEdit.text()+"'")
        dados_comanda = cursor.fetchall()
        valor = dados_comanda[0][0]
        nome = dados_comanda[0][1]
        forme.label.setText(forme.lineEdit.text())
        forme.label_3.setText(nome)
        forme.label_2.setText("R$ "+str(valor))

    
def janela_comanda():
    add.show()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+forme.lineEdit_3.text()+"'")
    dados_comanda = cursor.fetchall()
    valor_atual = dados_comanda[0][0]
    add.label_6.setText("R$ "+str(dados_comanda[0][0]))
    add.label_10.setText(dados_comanda[0][1])
    add.label.setText("N°: "+forme.lineEdit_3.text())

def confirmar_pedido():
    print("ok ate aqui!")
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
    # print(valor_atual)
    # print(sum(lista_preco))

    # nome = forme.lineEdit_4.text()
    saldo_final = valor_atual - soma
 
    # numero = int(forme.lineEdit_3.text())
    banco = conexao.cursor()
    cursor = conexao.cursor()
    # cursor.execute("UPDATE comandas SET valor = '{}' WHERE numero = {}".format(saldo_final, numero_comanda))
    cursor.execute(f"UPDATE comandas SET valor = '{saldo_final:.2f}' WHERE numero_comanda = {numero_comanda}")
    banco.close()
    add.label_5.setText("R$ 0.00")
    add.label_7.setText("R$ 0.00")
    lista_preco.clear()
    lista_produto.clear()
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
    numero_comanda = forme.lineEdit.text()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("UPDATE comandas SET valor = '{}', nome = '' WHERE numero_numero = {}".format(valor, numero_comanda))
    banco.close()
    
    forme.label_4.setText("Comanda "+numero_comanda+" foi zerada com sucesso!")
    forme.label.setText("")
    forme.label_3.setText("")
    forme.label_2.setText("")
    forme.lineEdit.setText("")
    forme.lineEdit_2.setText("")
    forme.lineEdit_4.setText("")
    listar_dados()

def erro():
    ero.close()
    cancelar()


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
        for j in range(0, 2):
            forme.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            
    
    # for i in range(1, len(dados_lidos)):
    #     for j in range(2, 3):
    #         forme.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem('Falta '+str(falta[0][i])))
    # forme.tableWidget.setItem(0, 2, QtWidgets.QTableWidgetItem('PRÓXIMO'))
    # print(dados_lidos[0][1])


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
# historico = uic.loadUi("historico.ui")
forme.show()

iniciar()
# threading.Thread(target=hora_atualiza).start()

add.pushButton.clicked.connect(add_produto)
forme.pushButton_7.clicked.connect(zerar)
add.pushButton_3.clicked.connect(cancelar)
forme.pushButton_2.clicked.connect(janela_comanda)
add.pushButton_2.clicked.connect(confirmar_pedido)
# forme.pushButton.clicked.connect(cantou)
forme.pushButton.clicked.connect(add_saldo)
forme.pushButton_3.clicked.connect(ler)
ero.pushButton.clicked.connect(erro)

app.exec_()


import datetime
from PyQt5 import uic, QtWidgets
import sqlite3
import time
import threading
import pymysql
import win32print
import win32api
import os
# import bcrypt
import util
# import keyboard


# data = datetime.datetime.now()
# data_str = data.strftime("%d/%m/%y")
# hora = datetime.datetime.now()
# hora_str = hora.strftime("%H:%M:%S") 
# data_hora = data.strftime("%y/%m/%d") + " " +hora_str

conexao = pymysql.connect(host='SERVIDOR',user='root', database='banco_dados', password='pindoba10')

lista_preco = []
lista_produto = []
id_produto = []

def iniciar():

    # nome = 'RAUL ROCK BAR'
    # banco = sqlite3.connect('config.db')
    # cursor = banco.cursor()
    # cursor.execute(
    #     "CREATE TABLE IF NOT EXISTS comandas (id INTEGER PRIMARY KEY AUTOINCREMENT, numero integer, valor REAL, nome text)")
    # cursor.execute("CREATE TABLE IF NOT EXISTS produtos (id INTEGER PRIMARY KEY AUTOINCREMENT, codigo integer, nome text, valor REAL )")
    # banco.commit()
    # banco.close()
    listar_produtos()
    
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
    nivel = user.spinBox.text()
    
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("INSERT INTO users (nome, senha, nivel) VALUES ('{}', '{}', '{}')".format(nome,senha,nivel))
    cursor.execute("commit;")
    banco.close()
    listar_user()

    user.label.setText("Usuário Cadastrado com sucesso!")
    
def cadastro_produto():

    codigo = user.lineEdit_4.text()
    nome = user.lineEdit_5.text()
    preco = user.lineEdit_6.text().replace(",",".")
    imprimir = user.checkBox.isChecked()

    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT count(codigo_produto)  as tem FROM banco_dados.produtos where codigo_produto ="+codigo+"")
    tem = cursor.fetchall()
    print(type(tem))
    print(tem[0][0])
    if tem[0][0] > 0:
        ero.show()
        ero.label.setText("Produto já cadastrado!")
        user.lineEdit_4.setText('')
    else:

        cursor.execute("INSERT INTO produtos (codigo_produto, nome, valor, imprimir) VALUES ({}, '{}', {},{})".format(codigo,nome,preco,imprimir))
        cursor.execute("commit;")
        banco.close()
        user.label_11.setText('Produto cadastrado com sucesso!')
        user.lineEdit_4.setText('')
        user.lineEdit_5.setText('')
        user.lineEdit_6.setText('')
        listar_produtos_cadastro()

def add_procurar():
    pesquisa = add_tabela.lineEdit.text()
    # banco = conexao.cursor()
    # cursor = conexao.cursor()
    # cursor.execute("SELECT nome  FROM banco_dados.produtos WHERE nome like  '%"+pesquisa+"%'")
    dados_lidos = util.banco( 'produtos',pesquisa,'nome').get()
    # dados_lidos = cursor.fetchall()
    add_tabela.tableWidget_2.setRowCount(len(dados_lidos))
    add_tabela.tableWidget_2.setColumnCount(1)
    # banco.close()
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 1):
            add_tabela.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def open_add():
    add_tabela.show()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome FROM produtos")
    dados_lidos = cursor.fetchall()
    add_tabela.tableWidget_2.setRowCount(len(dados_lidos))
    add_tabela.tableWidget_2.setColumnCount(1)
    banco.close()
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 1):
            add_tabela.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

# add produto da tela de pesquisa na tela de compra da comanda
def add_comanda():
    codigo = add_tabela.tableWidget_2.currentItem().text()
    print(codigo)
    cursor = conexao.cursor()
    cursor.execute(f"SELECT codigo_produto FROM produtos WHERE nome = '{codigo}'")
    dados_produto = cursor.fetchall()
    print(dados_produto[0][0])
    add.lineEdit.setText(str(dados_produto[0][0]))
    time.sleep(0.2)
    add_produto()


def editar_produto():
    try:
        codigo = user.tableWidget_2.currentItem().text()

        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM produtos where codigo_produto = "+codigo+" ")
        dados_produto = cursor.fetchall()
        # print(user.tableWidget_2.currentItem().text())

        user.lineEdit_4.setText(str(dados_produto[0][0]))
        user.lineEdit_3.setText(str(dados_produto[0][0]))
        user.lineEdit_5.setText(dados_produto[0][1])
        user.lineEdit_6.setText(str(dados_produto[0][2]))
        user.checkBox.setChecked(dados_produto[0][3])
    except:
        ero.show()
        ero.label.setText("Click somente sobre o código do produto que deseja editar.")


def salvar_edicao_produto():
    try:

        codigo_antigo = user.lineEdit_3.text()
        codigo = user.lineEdit_4.text()
        nome = user.lineEdit_5.text()
        valor = user.lineEdit_6.text()
        imprimir = user.checkBox.isChecked()

        banco = conexao.cursor()
        cursor = conexao.cursor()
        cursor.execute(f"UPDATE produtos SET codigo_produto = {codigo}, nome = '{nome}', valor = '{valor}', imprimir = {imprimir} WHERE codigo_produto = {codigo_antigo}")
        cursor.execute("commit;")
        banco.close()
        listar_produtos_cadastro()
        # lista_produto()
        user.lineEdit_4.setText('')
        user.lineEdit_5.setText('')
        user.lineEdit_6.setText('')
    except:
        ero.show()
        ero.label.setText("Algo deu errado!")


def add_produto():
    try:
        add.label_11.setText('')
        global lista_preco
        global lista_produto
        numero_comanda = forme.lineEdit_3.text()
        
        dados_comanda = util.Get('comandas',numero_comanda,'valor', 'numero_comanda').get()

        # cursor = conexao.cursor()
        # cursor.execute(f"SELECT valor FROM comandas WHERE numero_comanda ={numero_comanda}")
        # dados_comanda = cursor.fetchall()
        valor_atual = dados_comanda[0][0]   
        print(valor_atual)
        numero_produto = add.lineEdit.text()

        dados_produto = util.Get('produtos',numero_produto,'nome, valor, imprimir', 'codigo_produto').get()
        # cursor = conexao.cursor()
        # cursor.execute(f"SELECT nome, valor, imprimir FROM produtos WHERE codigo_produto = {numero_produto}")
        # dados_produto = cursor.fetchall()
        lista_produto.append(dados_produto[0][0])
        lista_preco.append(dados_produto[0][1])
        imprimir = dados_produto[0][2]
        if imprimir == True:
            id_produto.append(int(numero_produto))
        else:
            pass
        add.listWidget.addItem(dados_produto[0][0])
        add.listWidget_2.addItem("R$ "+str(dados_produto[0][1]))
        
        subtotal = sum(lista_preco)
        novo_valor = valor_atual - subtotal
        add.label_7.setText(" R$ "+str(novo_valor))
        add.label_5.setText(" R$ "+str(subtotal))
        add.lineEdit.setText("")
        if novo_valor < 0:
            ero.show()
            ero.label.setText("Saldo insuficiente.")

    except:
        add.label_11.setText('Produto não encontrado!')
        add.lineEdit.setText('')


def entrar_guarida():
    nome = forme.lineEdit_5.text()
    senha = forme.lineEdit_6.text()
    try:
        cursor = conexao.cursor()
        cursor.execute(f"SELECT senha, nome FROM users WHERE nome = '{nome}'")
        dados_user = cursor.fetchall()
        senha_verificada = util.verificar_senha(senha, dados_user[0][0])

        if nome == dados_user[0][1] and senha_verificada == True:
            forme.label.setText("")
            forme.lineEdit_5.setText('')
            forme.lineEdit_6.setText('')
            guarida.show()

        else:
            forme.label.setText("Usuário ou Senha incorreto")
    except:
        forme.label.setText("Usuário inexistente")

def alterar_nome():
    try:
        numero_comanda = forme.lineEdit_8.text()
        # banco = conexao.cursor()
        # cursor = conexao.cursor()
        # cursor.execute(f"SELECT nome FROM comandas WHERE numero_comanda = {numero_comanda}")
        # dados_comanda = cursor.fetchall()
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
    except:
        print('Erro')
        forme.label_4.setText("Comanda não encontrada")
        
def add_saldo():
    if guarida.lineEdit.text() != "" and guarida.lineEdit_2.text() != "":
        data = datetime.datetime.now()
        data_str = data.strftime("%d/%m/%y")
        hora = datetime.datetime.now()
        hora_str = hora.strftime("%H:%M:%S")
        data_hora = data.strftime("%y/%m/%d") + " " +hora_str
        
        dados_comanda = util.Get('comandas',guarida.lineEdit.text(), 'valor, nome','numero_comanda').get()
        # banco = conexao.cursor()
        # cursor = conexao.cursor()
        # cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+guarida.lineEdit.text()+"'")
        # dados_comanda = cursor.fetchall()
        valor_atual = dados_comanda[0][0]
        nome_db = dados_comanda[0][1]
        nome = guarida.lineEdit_4.text()
        valor_inserir = float(guarida.lineEdit_2.text().replace(",","."))
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
    try:
        if guarida.lineEdit.text() != "" or guarida.lineEdit_2.text() != "":
            dados_comanda = util.Get('comandas',guarida.lineEdit.text(),'valor, nome','numero_comanda').get()
            # banco = conexao.cursor()
            # cursor = conexao.cursor()
            # cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+guarida.lineEdit.text()+"'")
            # dados_comanda = cursor.fetchall()
            valor = dados_comanda[0][0]
            nome = dados_comanda[0][1]
            guarida.label.setText('Comanda: '+guarida.lineEdit.text())
            guarida.label_3.setText('Nome: '+nome)
            guarida.label_2.setText("Valor atual: R$ "+str(valor))
    except:
        guarida.label.setText('Comanda não encontrada')
        guarida.label_3.setText('')
        guarida.label_2.setText("")

def janela_comanda():
    try:
        forme.label_11.setText('')
        dados_comanda = util.Get('comandas',forme.lineEdit_3.text(),'valor, nome','numero_comanda').get()
        # banco = conexao.cursor()
        # cursor = conexao.cursor()
        # cursor.execute("SELECT valor, nome FROM comandas WHERE numero_comanda = '"+forme.lineEdit_3.text()+"'")
        # dados_comanda = cursor.fetchall()
        valor_atual = dados_comanda[0][0]
        add.show()
        lista_preco.clear()
        lista_produto.clear()
        add.label_5.setText("R$ 0.00")
        add.label_7.setText("R$ 0.00")
        add.listWidget.clear()
        add.listWidget_2.clear()
        add.label_6.setText("R$ "+str(dados_comanda[0][0]))
        add.label_10.setText(dados_comanda[0][1])
        add.label.setText("N°: "+forme.lineEdit_3.text())
    except:
        forme.label_11.setText('Comanda não encontrada!')
        # print('Comanda não encontrada!')

def confirmar_pedido():
    
    data = datetime.datetime.now()
    data_str = data.strftime("%d/%m/%y")
    hora = datetime.datetime.now()
    hora_str = hora.strftime("%H:%M:%S")
    data_hora = data.strftime("%y/%m/%d") + " " +hora_str
    numero_comanda = forme.lineEdit_3.text()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT valor FROM comandas WHERE numero_comanda = '"+numero_comanda+"'")
    dados_comanda = cursor.fetchall()
    valor_atual = dados_comanda[0][0]
    soma = sum(lista_preco)  
    saldo_final = valor_atual - soma

    if soma > valor_atual:
        ero.show()
        ero.label.setText("Saldo insuficiente.")
        add.close()
    else:

        cursor2 = conexao.cursor()
        cursor2.execute("SELECT nome FROM comandas WHERE numero_comanda = '"+numero_comanda+"'")
        nome_comanda = cursor2.fetchall()
        n = 0
        for i in id_produto:
                
            cursor = conexao.cursor()
            cursor.execute("SELECT nome FROM produtos WHERE codigo_produto = '"+str(id_produto[n])+"'")
            dados_comanda = cursor.fetchall()

            arquivo = open("print.txt", "w")
            arquivo.write("Comanda: "+numero_comanda)
            arquivo.write("\n\n"+dados_comanda[0][0]+"\n\n")
            arquivo.write(nome_comanda[0][0]+"\n\n")
            arquivo.write("HORA: "+hora_str)
            arquivo.write("\nDATA: "+ data_str)
            arquivo.write("\n          ...")
            arquivo.close()

            lista_impressoras = win32print.EnumPrinters(2)
            impressora = lista_impressoras[4]
            win32print.SetDefaultPrinter(impressora[2])
            win32api.ShellExecute(0, "print", "print.txt", None, ".", 0)
            n = n+1        
            time.sleep(0.7)

        banco = conexao.cursor()
        cursor = conexao.cursor()
        cursor.execute(f"UPDATE comandas SET valor = '{saldo_final:.2f}' WHERE numero_comanda = {numero_comanda}")
        cursor.execute("commit;")
        banco.close()
            
        add.close()
        listar_dados()
        indice = 0
        for i in lista_preco:
            cursor.execute("INSERT INTO historicos (evento, numero_comanda, nome, produto, valor, data) VALUES ('{}', '{}', '{}','{}', {}, '{}')".format("VENDA",forme.lineEdit_3.text(),add.label_10.text(), lista_produto[indice],lista_preco[indice], data_hora))
            cursor.execute("commit;")
            indice +=1

        add.label_5.setText("R$ 0.00")
        add.label_7.setText("R$ 0.00")
            
        add.listWidget.clear()
        add.listWidget_2.clear()
        forme.lineEdit_3.setText("")

        lista_preco.clear()
        lista_produto.clear()
        id_produto.clear()
        historico()

def cupom():
    global lista_preco
    global lista_produto

    n = 0
    arquivo = open("cupom.txt", "w")
    for i in range(len(lista_produto)):
        
        arquivo.write((str(lista_produto[n])+'__________')[0:16]+' R$ '+ str(lista_preco[n])+'\n')
        # arquivo.write("\n\n"+"\n\n")
        # arquivo.write(nome_comanda[0][0]+"\n\n")
        # arquivo.write("HORA: "+hora_str)
        # arquivo.write("\nDATA: "+ data_str)
        # arquivo.write("\n          ...")
        
        n += 1
    total = add.label_5.text()
    arquivo.write("\nTotal:      "+total[0:10]+"\n")
    arquivo.write("\n----CUPOM NÃO FISCAL----\n")

    
    arquivo.close()

    lista_impressoras = win32print.EnumPrinters(2)
    impressora = lista_impressoras[4]
    win32print.SetDefaultPrinter(impressora[2])
    win32api.ShellExecute(0, "print", "cupom.txt", None, ".", 0)

def cancelar():
    lista_preco.clear()
    lista_produto.clear()
    add.label_5.setText("R$ 0.00")
    add.label_7.setText("R$ 0.00")
    forme.lineEdit_3.setText("")
    add.listWidget.clear()
    add.listWidget_2.clear()
    add.label_11.setText('')
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
    nome = forme.lineEdit_9.text()
    senha = forme.lineEdit_10.text()
    try:
        cursor = conexao.cursor()
        cursor.execute(f"SELECT senha, nome, nivel FROM users WHERE nome = '{nome}'")
        dados_user = cursor.fetchall()
        senha_verificada = util.verificar_senha(senha, dados_user[0][0])
  
        if nome == dados_user[0][1] and senha_verificada == True and dados_user[0][2] == '3':
            forme.label_9.setText("")
            user.show()
            forme.lineEdit_9.setText('')
            forme.lineEdit_10.setText('')
            listar_user()
            time.sleep(0.3)
            listar_produtos_cadastro()

        else:
            forme.label_9.setText("Usuário ou Senha incorreto")
    except:
        forme.label_9.setText("Usuário inexistente")
    # user.show()

def listar_dados():
    get = util.Get('comandas','','*')
    dados_lidos = get.get_all()
    # banco = conexao.cursor()
    # cursor = conexao.cursor()
    # cursor.execute("SELECT * FROM comandas")
    # dados_lidos = cursor.fetchall()
    forme.tableWidget.setRowCount(len(dados_lidos))
    forme.tableWidget.setColumnCount(3)
    # banco.close()
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 3):
            forme.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            
    
    for i in range(0, len(dados_lidos)):
        for j in range(1, 2):
            forme.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem('R$  '+str(dados_lidos[i][j])))

def listar_user():
        banco = conexao.cursor()
        cursor = conexao.cursor()
        cursor.execute("SELECT nome, nivel FROM users")
        dados_lidos = cursor.fetchall()
        user.tableWidget.setRowCount(len(dados_lidos))
        user.tableWidget.setColumnCount(2)
        banco.close()
        
        for i in range(0, len(dados_lidos)):
            for j in range(0, 2):
                user.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))

def historico():
    dados_lidos = util.Get('historicos','','*').get_all()
    # banco = conexao.cursor()
    # cursor = conexao.cursor()
    # cursor.execute("SELECT * FROM historicos")
    # dados_lidos = cursor.fetchall()
    forme.tableWidget_3.setRowCount(len(dados_lidos))
    forme.tableWidget_3.setColumnCount(6)
    # banco.close()
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 6):
            forme.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
    for i in range(0, len(dados_lidos)):
            for j in range(4, 5):
                forme.tableWidget_3.setItem(i, j, QtWidgets.QTableWidgetItem('R$  '+str(dados_lidos[i][j])))  

def listar_produtos_cadastro():
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados_lidos = cursor.fetchall()
    user.tableWidget_2.setRowCount(len(dados_lidos))
    user.tableWidget_2.setColumnCount(3)
    banco.close()
    # lista_produto()
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 3):
            user.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            
    
    for i in range(0, len(dados_lidos)):
        for j in range(2, 3):
            user.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem('R$  '+str(dados_lidos[i][j])))  

def listar_produtos():
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM produtos")
    dados_lidos = cursor.fetchall()
    forme.tableWidget_2.setRowCount(len(dados_lidos))
    forme.tableWidget_2.setColumnCount(3)
    banco.close()
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 3):
            forme.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            
    
    for i in range(0, len(dados_lidos)):
        for j in range(2, 3):
            forme.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem('R$  '+str(dados_lidos[i][j])))         

def procurar_produto():
    pesquisa = forme.lineEdit_4.text()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT *  FROM banco_dados.produtos WHERE nome like  '%"+pesquisa+"%'")
    dados_lidos = cursor.fetchall()
    forme.tableWidget_2.setRowCount(len(dados_lidos))
    forme.tableWidget_2.setColumnCount(3)
    banco.close()
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 3):
            forme.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            
    
    for i in range(0, len(dados_lidos)):
        for j in range(2, 3):
            forme.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem('R$  '+str(dados_lidos[i][j])))
    
def procurar_produto_adm():
    pesquisa = user.lineEdit_5.text()
    banco = conexao.cursor()
    cursor = conexao.cursor()
    cursor.execute("SELECT *  FROM banco_dados.produtos WHERE nome like  '%"+pesquisa+"%'")
    dados_lidos = cursor.fetchall()
    user.tableWidget_2.setRowCount(len(dados_lidos))
    user.tableWidget_2.setColumnCount(3)
    banco.close()
    
    for i in range(0, len(dados_lidos)):
        for j in range(0, 3):
            user.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem(str(dados_lidos[i][j])))
            
    
    for i in range(0, len(dados_lidos)):
        for j in range(2, 3):
            user.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem('R$  '+str(dados_lidos[i][j])))
    
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


app = QtWidgets.QApplication([])
forme = uic.loadUi("comanda.ui")
add = uic.loadUi("add.ui")
ero = uic.loadUi("erro.ui")
user = uic.loadUi("user.ui")
guarida = uic.loadUi("guarida.ui")
add_tabela = uic.loadUi("add_tabela.ui")
# historico = uic.loadUi("historico.ui")
forme.show()

iniciar()
# threading.Thread(target=hora_atualiza).start()
forme.pushButton_7.clicked.connect(open_user)
forme.pushButton_4.clicked.connect(entrar_guarida)
forme.pushButton_2.clicked.connect(janela_comanda)
forme.pushButton_5.clicked.connect(alterar_nome)
forme.pushButton_3.clicked.connect(procurar_produto)


add.pushButton_2.clicked.connect(confirmar_pedido)
add.pushButton_3.clicked.connect(cancelar)
add.pushButton_4.clicked.connect(cupom)
add.pushButton_5.clicked.connect(open_add)
add.pushButton.clicked.connect(add_produto)

guarida.pushButton_7.clicked.connect(zerar)
guarida.pushButton.clicked.connect(add_saldo)
guarida.pushButton_3.clicked.connect(ler)

ero.pushButton.clicked.connect(erro)

user.pushButton.clicked.connect(salvar_user)
user.pushButton_3.clicked.connect(cadastro_produto)
user.pushButton_4.clicked.connect(editar_produto)
user.pushButton_5.clicked.connect(salvar_edicao_produto)
user.pushButton_10.clicked.connect(procurar_produto_adm)

add_tabela.pushButton.clicked.connect(add_procurar)
add_tabela.pushButton_5.clicked.connect(add_comanda)



# def key():
# #     while True:
#         keyboard.add_hotkey("esc",cancelar)
# #         time.sleep(1)
    


# threading.Thread(target=key).start()
app.exec_()


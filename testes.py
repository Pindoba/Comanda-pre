
from ast import Import
import pymysql
import datetime
import util
import threading
# import keyboard
import time
# def cancelar():
#     print('apertou')


# def key():
#     # while True:
#         keyboard.add_hotkey("esc",cancelar)
#         # time.sleep(2)
    


# threading.Thread(target=key).start()
# conexao = pymysql.connect(host='DESKTOP-IDQTBUT',user='root', database='banco_dados', password='pindoba10')



# banco = conexao.cursor()
# cursor = conexao.cursor()

# nome = 'fulano'
# nivel = '3'
# senha_entrada = util.criar_senha('123456')
# # print(senha_entrada)
# senha_replace = str(senha_entrada).replace("'","")
# # print(senha_replace)
# senha_pra_db = senha_replace[1:]



# cursor.execute("INSERT INTO users (nome, senha, nivel) VALUES ('{}', '{}', '{}')".format(nome,senha_pra_db,nivel))
# cursor.execute("commit;")
# banco.close()
# print(bytes(senha_pra_db, 'utf-8'))


# print(util.verificar_senha('123456',bytes(senha_pra_db, 'utf-8')))



# data = datetime.datetime.now()
# data_str = data.strftime("%d/%m/%y")
# hora = datetime.datetime.now()
# hora_str = hora.strftime("%H:%M")
# print(data)


pequisa = util.Get('comandas','101','valor','numero_comanda')
www = pequisa.get()

print(www)
# ("INSERT INTO historicos (evento, numero_comanda, nome, produto, valor, data) VALUES ('{}', '{}', '{}','{}', {}, '{}')".format("VENDA",forme.lineEdit_3.text(),add.label_10.text(), lista_produto[indice],lista_preco[indice], data_hora))


# post = util.Post("historicos","(evento, numero_comanda, nome, produto, valor, data)","('VENDA','102030','wellwell', 'caldo de bila', 5.6 ,'2022-10-17 16:32:52.000')")

# post.post()
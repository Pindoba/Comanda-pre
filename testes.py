
from ast import Import
import pymysql
import datetime
import util

conexao = pymysql.connect(host='DESKTOP-IDQTBUT',user='root', database='banco_dados', password='pindoba10')



banco = conexao.cursor()
cursor = conexao.cursor()

nome = 'fulano'
nivel = '3'
senha_entrada = util.criar_senha('123456')
# print(senha_entrada)
senha_replace = str(senha_entrada).replace("'","")
# print(senha_replace)
senha_pra_db = senha_replace[1:]



cursor.execute("INSERT INTO users (nome, senha, nivel) VALUES ('{}', '{}', '{}')".format(nome,senha_pra_db,nivel))
cursor.execute("commit;")
banco.close()
print(bytes(senha_pra_db, 'utf-8'))


print(util.verificar_senha('123456',bytes(senha_pra_db, 'utf-8')))







# data = datetime.datetime.now()
# data_str = data.strftime("%d/%m/%y")
# hora = datetime.datetime.now()
# hora_str = hora.strftime("%H:%M")
# print(data)

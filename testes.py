
import pymysql

# conexao = pymysql.connect(host='DESKTOP-IDQTBUT',user='root', database='banco_dados', password='pindoba10')

# print("tudo certo meu consagrado")


# # with conexao.cursor() as c:
# banco = conexao.cursor()
# sql = "select * from comandas"
# banco.execute(sql)
# res = banco.fetchall()
# print(res)
lista_id = [452,487,1001,32,1540,2,1245]
lista_imprimir = []
n = 0
for id in lista_id:
    if id > 1000 and id < 2000:
        print(n)
    else:
        n=n+1




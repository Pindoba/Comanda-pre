
import pymysql

conexao = pymysql.connect(host='DESKTOP-IDQTBUT',user='root', database='banco_dados', password='pindoba10')

print("tudo certo meu consagrado")


# with conexao.cursor() as c:
banco = conexao.cursor()
sql = "select * from comandas"
banco.execute(sql)
res = banco.fetchall()
print(res)

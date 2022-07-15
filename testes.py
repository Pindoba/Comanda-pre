
import pymysql

conexao = pymysql.connect(host='DESKTOP-IDQTBUT',user='root', database='banco_dados', password='pindoba10')

print("tudo certo meu consagrado")


with conexao.cursor() as c:
    sql = "select * from comandas"
    c.execute(sql)
    res = c.fetchall()
    print(res)


import pymysql
import bcrypt


class banco():
    def __init__( self, tabela, busca, coluna, condicao=None):
        self.conexao = pymysql.connect(host='SERVIDOR',user='root', database='banco_dados', password='pindoba10')
        self.cursor = self.conexao.cursor()
        self.busca = busca
        self.tabela = tabela
        self.coluna = coluna
        self.condicao = condicao

    # def get(self ):
    #     cursor = self.cursor
    #     cursor.execute(f"SELECT {self.coluna}  FROM {self.tabela} WHERE nome like  '%{self.busca}%'")
    #     dados_lidos = self.cursor.fetchall()
    #     cursor.close()
    #     return dados_lidos

    

class Get(banco):
    def __init__(self, tabela, busca, coluna, condicao=None):
        self.condicao = condicao
        

        super().__init__(tabela, busca, coluna, self.condicao)


    def get(self ):
        cursor = self.cursor
        cursor.execute(f"SELECT {self.coluna}  FROM {self.tabela} WHERE {self.condicao} =  {self.busca}")
        dados_lidos = self.cursor.fetchall()
        cursor.close()
        return dados_lidos

    def buscar(self):
        cursor = self.cursor
        cursor.execute(f"SELECT {self.coluna}  FROM {self.tabela} WHERE nome like  '%{self.busca}%'")
        dados_lidos = self.cursor.fetchall()
        cursor.close()
        return dados_lidos

    def get_all(self):
        cursor = self.cursor
        cursor.execute(f"SELECT {self.coluna}  FROM {self.tabela} ")
        dados_lidos = self.cursor.fetchall()
        cursor.close()
        return dados_lidos


class Post(banco):
    def __init__(self, tabela, campos, valores):
        self.campos = campos
        self.valores = valores
        
        
        super().__init__(tabela, self.campos, self.valores)


    def post(self):
        cursor = self.cursor
        # cursor.execute("INSERT INTO historicos (evento, numero_comanda, nome, produto, valor, data) VALUES('exenplo', '2136548', 'wewel', 'caldo de cana', 3.5, '2022-10-17 16:32:52.000')")

        cursor.execute(f"INSERT INTO {self.tabela} {self.campos} VALUES {self.valores}")
        cursor.execute("commit;")
        # dados_lidos = self.cursor.fetchall()
        
        cursor.close()
        
        return print('tudo certo!!\n', self.tabela,self.campos,self.valores)
   
        

    
        







def criar_senha(senha_login):

    return bcrypt.hashpw(bytes(senha_login, 'utf-8'), bcrypt.gensalt(10))
  

def verificar_senha(senha_login, senha_db):
    
    if bcrypt.hashpw(bytes(senha_login, 'utf-8'), senha_db) == senha_db:
        return True

    else:
        return False
# senha = (criar_senha('123'))
# senha = (str(criar_senha('123')).replace("'",""))
# senhadb = 
# senhadb = bytes('$2b$10$eL1rIRSysew8BiXhpBiySu5Y08Rdqqw4XOoZpSgPu9SsKBi/wpkSG','utf-8')
# print(senhadb)


# print(senha.replace("'",""))
# print(verificar_senha(senha,senhadb))


# print(criar_senha)
# entrar = str(input("Digite sua senha:\n"))
# senha_login = bytes(entrar, 'utf-8')








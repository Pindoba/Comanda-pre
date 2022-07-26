import bcrypt

def criar_senha(senha_login):

    return bcrypt.hashpw(bytes(senha_login, 'utf-8'), bcrypt.gensalt(10))
  



def verificar_senha(senha_login, senha_db):
    
    if bcrypt.hashpw(bytes(senha_login, 'utf-8'), senha_db) == senha_db:
        return True

    else:
        return False




# print(criar_senha)
# entrar = str(input("Digite sua senha:\n"))
# senha_login = bytes(entrar, 'utf-8')








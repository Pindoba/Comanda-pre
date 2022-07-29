import bcrypt

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








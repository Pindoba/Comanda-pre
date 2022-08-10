import sqlite3
import streamlit as st

import csv
import time
import os
# st.markdown('<html lang="pt-br" xml:lang="pt-br">')

st.set_page_config(page_title='Karaoke', page_icon=None, layout="centered", initial_sidebar_state="auto", menu_items=None)


def iniciar():
 
    nome = 'RAUL ROCK BAR'
    musica = ''
    banco = sqlite3.connect('nomes.db')
    cursor = banco.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS dados (id INTEGER PRIMARY KEY AUTOINCREMENT, nome text, musica text)")
    banco.commit()
    banco.close()
def karaoke():
    st.image('banner3.png')
    st.sidebar.image('logokaraoke.png', caption=None, width=300, use_column_width=True)
    st.sidebar.header('Selecione uma página')
    page = ['Inicio','Solicitar nome','Sobre o Karaoke']
    pagina_atual = st.sidebar.radio('',page)
    
    

    if pagina_atual == 'Inicio':
        st.title('Fila do Karaoke', anchor=False)
        banco = sqlite3.connect(r'\\192.168.18.57\Karaoke_2.0.2\banco_dados.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dados")
        dados_lidos = cursor.fetchall()
        banco.close()
        n = 0
        f = open('teste.txt','w')

        for i in dados_lidos:
            if n == 0:
                f.write(dados_lidos[n][1]+",Proximo,Já pode ir ao palco\n")
            else:
                f.write(dados_lidos[n][1]+",Falta "+str(n)+" pessoas,Média de "+str(n*5.75)+" minutos\n")
            n+=1
        f.close()

        linhas = csv.reader(open('teste.txt', 'r'))        
        st.table(linhas)
    elif pagina_atual == 'Solicitar nome':
        
    
        st.info('Lembrando que aqui é só um meio de solictar que seu nome entre na fila. Para isso será verificado se o nome já ta na fila e etc. Se o nome não se encontrar mais nessa lista provavelmente ja estará na fila. Qualquer dúvida só falar com "o carinha do som".')
        nome = st.text_input('Nome:', value="", max_chars=None, key=None, type="default", help=None, autocomplete=None, on_change=None, args=None, kwargs=None,  placeholder=None, disabled=False)
        musica = st.text_input('Musica: (opcional)')
        inserir = st.button('Inserir nome')

        banco = sqlite3.connect('nomes.db')
        cursor = banco.cursor()
        cursor.execute("SELECT * FROM dados")
        dados_lidos = cursor.fetchall()
        def tabela():
            st.table(dados_lidos)
        if inserir:
        
            if nome == '':
                st.warning('Necessario um nome!')
            else:
                # banco = sqlite3.connect('nomes.db')
                # cursor = banco.cursor()
                cursor.execute("INSERT INTO dados (nome, musica) VALUES ('" + nome + "', '" + musica + "')")
                banco.commit()
                cursor.execute("SELECT * FROM dados")
                dados_lidos = cursor.fetchall()
                

                banco.close()
                st.success("Solicitação feita com sucesso. Acompanhe a fila do karaoke para ver sua posição.")

        
        tabela()

        indice = st.number_input('ID', min_value=None, max_value=None, value=1)
        senha = st.text_input('Senha:', value="", max_chars=None, key=None, type="password", help=None, autocomplete=None, on_change=None, args=None, kwargs=None,  placeholder=None, disabled=False)
        apagar = st.button(label = 'Apagar nome', help = 'Somente para o ADM.')
        if senha == 'pindoba' and apagar:
            cursor.execute("DELETE FROM dados WHERE id=" + str(indice))
            banco.commit()
            banco.close()
        elif senha != 'pindoba' and apagar:
            st.error('Senha incorreta')
        

    elif pagina_atual == 'Sobre o Karaoke':
        # st.image('logokaraoke.png', caption=None, width=300)
        st.header('Horários:')

        st.write('Quinta-feira - 22h as 2h')
        st.write('Domingo - 19:30 as 0h')
        st.header('Fonte dos videos:')
        st.write('YouTube')
        st.header('Qrcode da pagina:')
        st.image('qrcode.jpg')
        # st.bar_chart()
        # st.snow()
        # st.balloons()
        # with st.spinner('Wait for it...'):
        #     time.sleep(5)
        # st.success('Done!')

    elif pagina_atual == 'welton':
        st.write('tudo certo manolo')


    # st.sidebar.button(label = 'Lista Karaokê', help = 'Visualiza a fila do karaoke')

    # if st.sidebar.button('Horários'):
    # st.sidebar.write('Quinta-feira - 22h as 2h')
    # st.sidebar.write('Domingo - 19:30 as 0h')
    # else:
    #      st.write('')
iniciar()
karaoke()

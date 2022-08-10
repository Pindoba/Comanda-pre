# import win32print
# import win32api
# import os

# escolher qual impressora a gente vai querer usar
# lista_impressoras = win32print.EnumPrinters(2)
# impressora = lista_impressoras[4]

# print(lista_impressoras)

# win32print.SetDefaultPrinter(impressora[2])
# # mandar imprimir todos os arquivos de uma pasta
# caminho = r"C:\Users\Raul Rock Bar\3D Objects\teste print"
# # print(caminho)
# # lista_arquivos = os.listdir(caminho)

# win32api.ShellExecute(0, "print", "print.txt", None, ".", 0)

# https://docs.microsoft.com/en-us/windows/win32/api/shellapi/nf-shellapi-shellexecutea
# for arquivo in lista_arquivos:
#     win32api.ShellExecute(0, "open", arquivo, None, caminho, 0)




from io import BytesIO

from barcode import EAN13
from barcode.writer import ImageWriter




# Write to a file-like object:
rv = BytesIO()
EAN13(str(100000902922), writer=ImageWriter()).write(rv)

# Or to an actual file:
with open("somefile.jpeg", "wb") as f:
    EAN13("100dfg11111", writer=ImageWriter()).write(f)
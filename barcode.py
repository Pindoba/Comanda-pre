from io import BytesIO
from barcode import EAN13 
from barcode.writer import ImageWriter

comanda = 100
for i in range(3):
    rv = BytesIO()
    EAN13('0'+str(comanda+'20092014'), writer=ImageWriter()).write(rv)

    with open(str(comanda)+".jpeg", "wb") as f:
        EAN13("100000011111", writer=ImageWriter()).write(f)

    comanda +=1
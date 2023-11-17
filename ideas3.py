import qrcode
from time import time, localtime, strftime


def crear_qr()->None:
    pelicula = 'Batman-'
    cine = 'Caballito-'
    entradas = '5-'
    tiempo = fecha_y_hora()
    img = qrcode.make(pelicula + cine + entradas + tiempo)
    img.save("Prueba 4.png")

def fecha_y_hora()->None:
    estructura = localtime()
    return strftime('%Y-%m-%d %H:%M:%S', estructura)

def main():
    crear_qr()
main()
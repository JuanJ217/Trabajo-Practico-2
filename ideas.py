import qrcode
from time import localtime, strftime
from requests import get

def obtener_informacion()->dict:

    url = "http://vps-3701198-x.dattaweb.com:4000/snacks"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    response = get(url, headers=headers)
    return response.json()


'''def fecha_y_hora()->None:
    estructura = localtime()
    return strftime('%Y-%m-%d %H:%M:%S', estructura)

def crear_qr()->None:
    pelicula = 'Batman-'
    cine = 'Caballito-'
    entradas = '5-'
    tiempo = fecha_y_hora()
    img = qrcode.make(pelicula + cine + entradas + tiempo)
    img.save("Prueba 4.png")'''

def main():
    print(obtener_informacion())
main()
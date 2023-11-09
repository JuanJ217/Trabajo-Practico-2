import requests
from tkinter import Entry, Button, Label, Tk

def obtener_snacks()->dict:

    url = "http://vps-3701198-x.dattaweb.com:4000/snacks"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}

    response = requests.get(url, headers=headers)

    return response.json() #Retorna una diccionario ya traducido de Json
    
def listar_snacks(snacks:dict, lista_final:list[str])->list[str]:
    for snack in snacks:
        lista_final.append(snack)

def ventana_de_reservas(lista_de_snakcs:list[str])->None:

    ventana_3 = Tk()
    ventana_3.geometry('720x480')
    ventana_3.config(bg='black')


    Lbl = Label(ventana_3, text= "\n".join(lista_de_snakcs))
    Lbl.pack()

    ventana_3.mainloop()


def main():

    lista_de_snacks:list[str]=[]
    listar_snacks(obtener_snacks(),lista_de_snacks)
    ventana_de_reservas(lista_de_snacks)
    print(lista_de_snacks)

main()
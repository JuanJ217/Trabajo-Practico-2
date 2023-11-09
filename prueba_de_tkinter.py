import requests
from tkinter import Entry, Button, Label, Tk

snacks:str='snacks'
movies:str='movies'

def obtener_snacks(objetivo)->dict:
    url = "http://vps-3701198-x.dattaweb.com:4000/" + objetivo
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    return response.json() #Retorna una diccionario ya traducido de Json
    

def listar_snacks(snacks:dict, lista_final:list[str])->None:
    for snack in snacks:
        lista_final.append(snack)

def cantidad_de_snacks(lista_snacks, contador_de_snacks)->None:
    for snacks in lista_snacks:
        contador_de_snacks[snacks]=0

def cerrar_ventana(ventana)->None:
    ventana.destroy()

def incrementar_snacks(snack, contador_de_snacks)->None:
    contador_de_snacks[snack]+=1
    actualizar_cantidad()

def decrementar_snacks(snack, contador_de_snacks)->None:
    if contador_de_snacks[snack]>0:
        contador_de_snacks[snack]-=1
        actualizar_cantidad()

def actualizar_cantidad(snacks, contador_de_snacks)->None:
    for snack in snacks:
        contador_de_snacks[snack].config(text=f'{snack} {contador_de_snacks[snack]}')

def ventana_de_reservas(snacks:list[str], contador_de_snacks:dict)->None:

    ventana = Tk()
    ventana.geometry('300x150')
    ventana.title('')
    ventana.resizable(width=False, height=False)

    comprar_entradas = Label(ventana, text='SECCION DE RESERVAS')
    comprar_entradas.pack()

    entrada = Label(ventana, text='Cantidad de entradas')
    entrada.pack()
    entrada.place(x=20, y=20)

    opciones_snacks = Button(ventana, text='Añadir snacks', command=lambda: ventana_de_snacks(snacks, contador_de_snacks))
    opciones_snacks.pack()
    opciones_snacks.place(x=60, y=70)

    terminar_compra = Button(ventana, text='Finalizar')
    terminar_compra.pack()
    terminar_compra.place(x=150, y=70)

    restar_cantidad = Button(ventana, text='- 1')
    restar_cantidad.pack()

    sumar_cantidad = Button(ventana, text='+1')
    sumar_cantidad.pack()
    sumar_cantidad.place(x=160, y=21)

    cancelar = Button(ventana, text='Cancelar compra', command=lambda: cerrar_ventana(ventana))
    cancelar.pack()

    ventana.mainloop()

def ventana_de_snacks(lista_de_snacks:list[str], contador_de_snacks:dict)->None:
    ventana_3 = Tk()
    ventana_3.geometry('200x300')
    ventana_3.resizable(width=False, height=False)

    #presentar
    espacios=0
    for snacks in lista_de_snacks:
        nombrar_snack = Label(ventana_3, text=f'{snacks} (0)', width=12, height=2)
        nombrar_snack.pack()
        nombrar_snack.place(x=0, y=espacios)
        espacios=+espacios+30
        contador_de_snacks[snacks] = nombrar_snack

    #restar
    espacios=5
    for snacks in lista_de_snacks:
        restar_snack = Button(ventana_3, text='-1', width=1, height=1)
        restar_snack.pack()
        restar_snack.place(x=88, y=espacios)
        espacios=+espacios+30

    #sumar
    espacios=5
    for snacks in lista_de_snacks:
        sumar_snack = Button(ventana_3, text='+1', width=1, height=1, command=lambda: incrementar_snacks(snacks, contador_de_snacks))
        sumar_snack.pack()
        sumar_snack.place(x=105, y=espacios)
        espacios=+espacios+30

    aceptar = Button(ventana_3, text='Aceptar')
    aceptar.pack()
    aceptar.place(x=75, y=220)

    cancelar = Button(ventana_3, text='Cancelar compra', command=lambda: cerrar_ventana(ventana_3))
    cancelar.pack()
    cancelar.place(x=50, y=250)

    ventana_3.mainloop()


def main():
    contador_de_snacks:dict={}
    lista_de_snacks:list[str]=[]
    listar_snacks(obtener_snacks(snacks),lista_de_snacks)
    ventana_de_reservas(lista_de_snacks, contador_de_snacks)

main()
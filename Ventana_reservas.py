import requests
from tkinter import Entry, Button, Label, Tk, Frame

snacks:str='snacks'
movies:str='movies'

def obtener_snacks(objetivo)->dict:
    url = "http://vps-3701198-x.dattaweb.com:4000/" + objetivo
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    return response.json() #Retorna una diccionario ya traducido de Json


def actualizar_datos_cines()->None:
    pass #Con esta función actualizaré la cantidad de asientos que haya para cada función de cada cine

    
def cantidad_de_snacks(informacion_snacks, contador_de_snacks)->None:
    for snack in informacion_snacks:
        contador_de_snacks[snack]=0


def cancelar_compra_snacks(contador_de_snacks, ventana, cantidad_visible)->None:
    for snack in contador_de_snacks:
        contador_de_snacks[snack]=0
        cantidad_visible.config(text=f'{snack} (0)')
    ventana.destroy()


#boletos = {'disponibles': x, 'totales': y, 'adquiridos': y-x, 'comprando':0}m
def aumentar_boletos(boletos, comprar_boleto, entrada)->None:
    for cantidad in comprar_boleto:
        if comprar_boleto[cantidad] < boletos['disponibles']:
            comprar_boleto[cantidad]+=1
            entrada.config(text=f'{comprar_boleto[cantidad]}')


def disminuir_boletos(comprar_boletos, entrada)->None:
    for cantidad in comprar_boletos:
        if comprar_boletos[cantidad]>0:
            comprar_boletos[cantidad]-=1
            entrada.config(text=f'{comprar_boletos[cantidad]}')
        

def cerrar_ventana(ventana)->None:
    ventana.destroy()


def aumentar_snacks(snack, contador_de_snacks, cantidad_visible)->None:
    contador_de_snacks[snack]+=1
    cantidad_visible.config(text=f'{snack} ({contador_de_snacks[snack]})')


def disminuir_snacks(snack, contador_de_snacks, cantidad_visible)->None:
    if contador_de_snacks[snack]>0:
        contador_de_snacks[snack]-=1
        cantidad_visible.config(text=f'{snack} ({contador_de_snacks[snack]})')


def ventana_de_reservas(contador_de_snacks:dict, informacion_snacks, boletos:dict, comprar_boleto:dict)->None:

    ventana = Tk()
    ventana.geometry('300x150')
    ventana.title('')
    ventana.resizable(width=False, height=False)

    comprar_entradas = Label(ventana, text='SECCION DE RESERVAS')
    comprar_entradas.pack()

    entrada = Label(ventana, text=f'disponibles')
    entrada.pack()
    entrada.place(x=20, y=20)

    opciones_snacks = Button(ventana, text='Añadir snacks', command=lambda: ventana_de_snacks(contador_de_snacks, informacion_snacks))
    opciones_snacks.pack()
    opciones_snacks.place(x=60, y=70)

    terminar_compra = Button(ventana, text='Finalizar')
    terminar_compra.pack()
    terminar_compra.place(x=150, y=70)

    restar_cantidad = Button(ventana, text='- 1', command=lambda: disminuir_boletos(comprar_boleto, entrada))
    restar_cantidad.pack()

    sumar_cantidad = Button(ventana, text='+1', command=lambda: aumentar_boletos(boletos, comprar_boleto, entrada))
    sumar_cantidad.pack()
    sumar_cantidad.place(x=160, y=21)

    cancelar = Button(ventana, text='Cancelar compra', command=lambda: cerrar_ventana(ventana))
    cancelar.pack()

    ventana.mainloop()


def ventana_de_snacks(contador_de_snacks:dict, informacion_snacks:dict)->None:

    ventana3 = Tk()
    ventana3.geometry('250x300')
    ventana3.config(bg='black')
    ventana3.resizable(width=False, height=False)

    encabezado = Label(ventana3, text='COMPRAR SNACKS')
    encabezado.pack(side='top')
    encabezado.config(fg='white', bg='black')

    for snack in informacion_snacks:
        posiciones = Frame(ventana3)
        posiciones.pack(side='top', anchor='w')
        posiciones.config(bg='black')

        cantidad_visible = Label(posiciones, text=f'{snack} ({contador_de_snacks[snack]})')
        sumar = Button(posiciones, text='- 1', command=lambda s=snack, c=cantidad_visible: disminuir_snacks(s, contador_de_snacks, c))
        restar = Button(posiciones, text='+1', command=lambda s=snack, c=cantidad_visible: aumentar_snacks(s, contador_de_snacks, c))
        precios = Label(posiciones, text=f'${informacion_snacks[snack]}')

        cantidad_visible.pack(side='left', anchor='w')
        cantidad_visible.config(width=15, fg='white', bg='black')
        sumar.pack(side='left')
        sumar.config(fg='white', bg='black')
        restar.pack(side='left')
        restar.config(fg='white', bg='black')
        precios.pack(side='left')
        precios.config(width=12, fg='white', bg='black')

    aceptar = Button(ventana3, text='Aceptar', command=lambda: cerrar_ventana(ventana3))
    aceptar.pack()
    aceptar.place(x=95, y=220)

    cancelar = Button(ventana3, text='Cancelar compra', command=lambda: cancelar_compra_snacks(contador_de_snacks, ventana3, cantidad_visible))
    cancelar.pack()
    cancelar.place(x=70, y=250)

    ventana3.mainloop()


def ventana_confirmar_compra()->None:
    pass


def main():
    boletos = {'disponibles': 5, 'totales': 10}
    comprar_boleto = {'cantidad': 0}
    informacion_snacks:dict = obtener_snacks(snacks)
    contador_de_snacks:dict={}
    cantidad_de_snacks(informacion_snacks, contador_de_snacks)
    ventana_de_reservas(contador_de_snacks, informacion_snacks, boletos, comprar_boleto)
    print(contador_de_snacks)

main()
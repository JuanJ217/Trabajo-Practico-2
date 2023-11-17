import requests
from tkinter import Button, Label, Tk, Frame, Canvas

PRECIO_DE_ENTRADA:int=1800
cantidad='cantidad'
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


def cancelar_compra_boletos(comprar_boleto, ventana1, entrada):
    for cantidad in comprar_boleto:
        comprar_boleto[cantidad]=0
        entrada.config(text=f'Cantidad de entradas ({comprar_boleto[cantidad]})')
    ventana1.destroy()
    
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


def ventana_de_reservas(contador_de_snacks:dict, informacion_snacks, boletos:dict, comprar_boleto:dict, lista_final)->None:

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

    terminar_compra = Button(ventana, text='Finalizar', command=lambda: ventana_confirmar_compra(informacion_snacks, contador_de_snacks, boletos, comprar_boleto, lista_final))
    terminar_compra.pack()
    terminar_compra.place(x=150, y=70)

    restar_cantidad = Button(ventana, text='- 1', command=lambda: disminuir_boletos(comprar_boleto, entrada))
    restar_cantidad.pack()

    sumar_cantidad = Button(ventana, text='+1', command=lambda: aumentar_boletos(boletos, comprar_boleto, entrada))
    sumar_cantidad.pack()
    sumar_cantidad.place(x=160, y=21)

    cancelar = Button(ventana, text='Cancelar compra', command=lambda: cancelar_compra_boletos(comprar_boleto, ventana, entrada))
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
        restar = Button(posiciones, text='- 1', command=lambda s=snack, c=cantidad_visible: disminuir_snacks(s, contador_de_snacks, c))
        sumar = Button(posiciones, text='+1', command=lambda s=snack, c=cantidad_visible: aumentar_snacks(s, contador_de_snacks, c))
        precios = Label(posiciones, text=f'${informacion_snacks[snack]}')

        cantidad_visible.pack(side='left', anchor='w')
        cantidad_visible.config(width=15, fg='white', bg='black')
        restar.pack(side='left')
        restar.config(fg='red')
        sumar.pack(side='left')
        sumar.config(fg='blue')
        precios.pack(side='left')
        precios.config(width=12, fg='white', bg='black')

    aceptar = Button(ventana3, text='Aceptar', command=lambda: cerrar_ventana(ventana3))
    aceptar.pack()
    aceptar.place(x=95, y=220)
    aceptar.config(fg='blue')

    cancelar = Button(ventana3, text='Cancelar compra', command=lambda: cancelar_compra_snacks(contador_de_snacks, ventana3, cantidad_visible))
    cancelar.pack()
    cancelar.place(x=70, y=250)
    cancelar.config(fg='red')

    ventana3.mainloop()

def ventana_confirmar_compra(informacion_snacks, contador_de_snacks, boletos, boleto_comprado, lista_final)->None:
    ventana_final = Tk()
    ventana_final.geometry('500x500')
    ventana_final.config(bg='black')

    encabezado = Label(ventana_final, text='CONFIRMACION DE COMPRA')
    encabezado.pack(side='top')
    encabezado.config(fg='white', bg='black')

    for cantidades_snacks in contador_de_snacks:
        cantidades = Frame(ventana_final)
        cantidades.pack(side='top', anchor='w')
        cantidades.config(bg='black')
        
        if contador_de_snacks[cantidades_snacks] > 0:
            snacks_seleccionados = Label(cantidades, text=f'{contador_de_snacks[cantidades_snacks]} {cantidades_snacks}')
            precio_snacks_seleccionados = Label(cantidades, text= precio_por_snack(cantidades_snacks, contador_de_snacks, informacion_snacks, lista_final))

            snacks_seleccionados.pack(side='left', anchor='w')
            snacks_seleccionados.config(width=15, fg='orange', bg='black')
            precio_snacks_seleccionados.pack(side='left')
            precio_snacks_seleccionados.config(fg='green', bg='black')

        if cantidades_snacks==list(contador_de_snacks.keys())[-1]:

            '''linea_separadora = Frame(cantidades, height=2, bg='yellow')
            linea_separadora.pack(fill='x')'''

            cantidad_boletos = Label(cantidades, text=f'{boleto_comprado[cantidad]} Entradas')
            precio_boletos_seleccionados = Label(cantidades, text=f'{boleto_comprado[cantidad] * PRECIO_DE_ENTRADA}')
            total = Label(cantidades, text=f'Total')
            precio_total = Label(cantidades, text=precio_final(lista_final))

            cantidad_boletos.pack(side='left',  anchor='w')
            cantidad_boletos.config(width=15, fg='orange', bg='black')
            precio_boletos_seleccionados.pack(side='left')
            precio_boletos_seleccionados.config(fg='green', bg='black')
            total.pack(side='left', anchor='w')
            total.config(width=15, fg='orange', bg='black')
            precio_total.pack(side='left')
            precio_total.config(width=15, fg='green', bg='black')

            

    ventana_final.mainloop()
    
def precio_por_snack(nombre_snack, cantidad_snack, precio_snack, lista_final)->str:
    precio_final = cantidad_snack[nombre_snack] * float(precio_snack[nombre_snack])
    lista_final.append(precio_final)
    return str(precio_final)


def precio_final(lista_final)->str:
    total=0
    for precios in lista_final:
        total+=precios
    return total
    


def main():
    lista_precio_comprador=[]
    boletos= {'disponibles': 5, 'totales': 10}
    boleto_comprado = {'cantidad': 0}
    informacion_snacks:dict = obtener_snacks(snacks)
    contador_de_snacks:dict={}
    cantidad_de_snacks(informacion_snacks, contador_de_snacks)
    ventana_de_reservas(contador_de_snacks, informacion_snacks, boletos, boleto_comprado, lista_precio_comprador)
    print(informacion_snacks)
    print(contador_de_snacks)
    print(boleto_comprado)
main()
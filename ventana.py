from tkinter import Button, Label, Tk, Frame
import requests
import qrcode
import timestamp



PRECIO_DE_ENTRADA:int=1800.00
cantidad:str= 'cantidad'
snacks:str= 'snacks'
movies:str = 'movies'

def obtener_snacks(objetivo)->dict:
    url = "http://vps-3701198-x.dattaweb.com:4000/" + objetivo
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    return response.json() #Retorna una diccionario ya traducido de Json


def actualizar_datos_cines()->None:
    pass #Con esta función actualizaré la cantidad de asientos que haya para cada función de cada cine


def recivir_datos_de_pelicula()->None:
    pass
    
def cantidad_de_snacks(informacion_snacks, contador_de_snacks)->None:
    for snack in informacion_snacks:
        contador_de_snacks[snack]=0


def reiniciar_snacks(contador_de_snacks, ventana, cantidad_visible)->None:
    for snack in contador_de_snacks:
        contador_de_snacks[snack]=1
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


def ventana_de_reservas(boletos:dict, comprar_boleto:dict, lista_final)->None:

    informacion_snacks:dict = obtener_snacks(snacks)
    contador_de_snacks:dict={}
    cantidad_de_snacks(informacion_snacks, contador_de_snacks)

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

    terminar_compra = Button(ventana, text='Carrito', command=lambda: ventana_confirmar_compra(informacion_snacks, contador_de_snacks, boletos, comprar_boleto, lista_final, ventana))
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
        cantidad_visible.pack(side='left', anchor='w')
        cantidad_visible.config(width=15, fg='white', bg='black')

        restar = Button(posiciones, text='- 1', command=lambda s=snack, c=cantidad_visible: disminuir_snacks(s, contador_de_snacks, c))
        restar.pack(side='left')
        restar.config(fg='red')

        sumar = Button(posiciones, text='+1', command=lambda s=snack, c=cantidad_visible: aumentar_snacks(s, contador_de_snacks, c))
        sumar.pack(side='left')
        sumar.config(fg='blue')

        precios = Label(posiciones, text=f'${informacion_snacks[snack]}')
        precios.pack(side='left')
        precios.config(width=12, fg='white', bg='black')

    aceptar = Button(ventana3, text='Aceptar', command=lambda: cerrar_ventana(ventana3))
    aceptar.pack()
    aceptar.place(x=95, y=220)
    aceptar.config(fg='blue')

    cancelar = Button(ventana3, text='Cancelar compra', command=lambda: reiniciar_snacks(contador_de_snacks, ventana3, cantidad_visible))
    cancelar.pack()
    cancelar.place(x=70, y=250)
    cancelar.config(fg='red')

    ventana3.mainloop()

def ventana_confirmar_compra(informacion_snacks, contador_de_snacks, boletos, boleto_comprado, lista_final, ventana)->None:

    cerrar_ventana(ventana)

    ventana_final = Tk()
    ventana_final.geometry('300x400')
    ventana_final.config(bg='black')
    ventana_final.resizable(width=False, height=False)

    encabezado = Label(ventana_final, text='CARRITO', font=20)
    encabezado.pack(side='top', pady=10)
    encabezado.config(fg='white', bg='black')

    for cantidades_snacks in contador_de_snacks:
        cantidades = Frame(ventana_final)
        cantidades.pack(side='top', anchor='w')
        cantidades.config(bg='black')
        
        if contador_de_snacks[cantidades_snacks] > 0:
            
            snacks_seleccionados = Label(cantidades, text=f'{contador_de_snacks[cantidades_snacks]} {cantidades_snacks}', font=20)
            snacks_seleccionados.pack(side='left')
            snacks_seleccionados.config(width=20, fg='orange', bg='black')

            precio_snacks_seleccionados = Label(cantidades, text= precio_por_snack(cantidades_snacks, contador_de_snacks, informacion_snacks, lista_final), font=20)
            precio_snacks_seleccionados.pack(side='left')
            precio_snacks_seleccionados.config(fg='green', bg='black')

    tickets = Frame(ventana_final)
    tickets.pack(side='top', anchor='w')
    tickets.config(bg='black')

    cantidad_boletos = Label(tickets, text=f'{boleto_comprado[cantidad]} Entradas', font=20)
    cantidad_boletos.pack(side='left',  anchor='w')
    cantidad_boletos.config(width=20, fg='orange', bg='black')

    precio_boletos_seleccionados = Label(tickets, text=precio_boletos(boleto_comprado), font=20)
    precio_boletos_seleccionados.pack(side='left')
    precio_boletos_seleccionados.config(fg='green', bg='black')

    linea_final = Frame(ventana_final)
    linea_final.pack(side='top', anchor='w', pady=15)
    linea_final.config(bg='black')

    palabra_total = Label(linea_final, text='TOTAL', font=20)
    palabra_total.pack(side='left', anchor='w')
    palabra_total.config(width=20, fg='red', bg='black')

    precio_total = Label(linea_final, text=precio_final(lista_final, boleto_comprado), font=20)
    precio_total.pack(side='left')
    precio_total.config(fg='green', bg='black')

    botones_de_accion = Frame(ventana_final)
    botones_de_accion.pack(side='top', anchor='center', pady=10)
    botones_de_accion.config(bg='black')

    boton_comprar = Button(botones_de_accion, text='PAGAR', command=None)
    boton_comprar.pack(side='top', anchor='n', pady=10)

    boton_cancelar_compra = Button(botones_de_accion, text='CANCELAR', command=None)
    boton_cancelar_compra.pack(side='bottom', anchor='center')  

    ventana_final.mainloop()

def precio_boletos(boleto_comprado)->str:
    return str(boleto_comprado[cantidad]*PRECIO_DE_ENTRADA)


def precio_por_snack(nombre_snack, cantidad_snack, precio_snack, lista_final)->str:
    precio_final = cantidad_snack[nombre_snack] * float(precio_snack[nombre_snack])
    lista_final.append(precio_final)
    return str(precio_final)


def precio_final(lista_final, boleto_comprado)->str:
    boletos=float(precio_boletos(boleto_comprado))
    total=0
    for precios in lista_final:
        total+=precios
    return str(total+boletos)

def crear_qr():
    pass
    


def main():
    lista_precio_comprador=[]
    boletos= {'disponibles': 5, 'totales': 10}
    boleto_comprado = {'cantidad': 0}
    ventana_de_reservas(boletos, boleto_comprado, lista_precio_comprador)
main()
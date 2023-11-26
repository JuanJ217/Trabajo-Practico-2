from tkinter import Tk, Label, Button, Frame, Entry, Toplevel, Canvas, Scrollbar, messagebox, filedialog
import tkinter as tk
from PIL import ImageTk, Image
import base64
import requests
import cv2
import qrcode
from time import localtime, strftime
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import PyPDF2
import fitz
from pyzbar.pyzbar import decode
import io

PRECIO_DE_ENTRADA:int=1800.00
cantidad:str= 'cantidad'
snacks:str= 'snacks'
movies:str = 'movies'
cinemas:str = 'cinemas'
opcion_de_cinema:str = 'Caballito'



def obtener_cantidad_asientos(objetivo)-> int:

    url = "http://vps-3701198-x.dattaweb.com:4000/" + objetivo
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    lista_de_cinemas = response.json()

    for informacion_cinemas in lista_de_cinemas:
        if informacion_cinemas['location'] == opcion_de_cinema:
            return informacion_cinemas['available_seats'] #32 asientos


def actualizar_datos_cines()-> None:
    #Con esta función actualizaré la cantidad de asientos que haya para cada función de cada cine
    pass


def recivir_datos_de_pelicula()-> None:
    pass
  
#--------------------------------------------------------------------CERRAR_VENTANA---------------------------------------------------------------#

def cerrar_ventana(ventana)-> None:

    ventana.destroy()

#--------------------------------------------------------------CONFIRMAR_COMPRA-------------------------------------------------------------------#

def ventana_confirmar_compra( informacion_snacks, contador_de_snacks, boletos,
                              boleto_comprado, lista_final, ventana3, ventana2,
                              dict_menu )-> None:

    if boleto_comprado['cantidad'] == 0:
        ventana3.withdraw()
        messagebox.showwarning('Advertencia', 'No hay boletos seleccionados')
        ventana3.deiconify()
    else:
        ventana3.withdraw()

        ventana_final = Toplevel()
        ventana_final.geometry('300x400')
        ventana_final.config(bg='black')
        ventana_final.resizable(width=False, height=False)

        encabezado = Label(
                                ventana_final, text='CARRITO', 
                                font=20, fg='white', bg='black'
                          )
        encabezado.pack(side='top', pady=10)
        
        snacks_comprados(contador_de_snacks, ventana_final, informacion_snacks, lista_final)
        boletos_comprados(ventana_final, boleto_comprado)
        mostrar_precio_total(ventana_final, lista_final, boleto_comprado)

        botones_de_accion = Frame(ventana_final,bg='black')
        botones_de_accion.pack(side='top', anchor='center', pady=10)
       
        boton_comprar = Button(
                                    botones_de_accion, text='PAGAR', 
                                    command=lambda: crear_qr(boleto_comprado, dict_menu, ventana_final,
                                                             ventana3, ventana2, contador_de_snacks)
                              )
        boton_comprar.pack(side='top', anchor='n', pady=10)

        boton_cancelar_compra = Button(
                                        botones_de_accion, text='CANCELAR', command=None
                                      )
        boton_cancelar_compra.pack(side='bottom', anchor='center')  

        ventana_final.mainloop()

#--------------------------------------------------------------CANTIDAD_SNACKS--------------------------------------------------------------------#

def cantidad_de_snacks(informacion_snacks, contador_de_snacks)-> None:

    for snack in informacion_snacks:
        contador_de_snacks[snack]=0

#------------------------------------------------------------------REINICIAR_SNACKS---------------------------------------------------------------#

def reiniciar_snacks(contador_de_snacks, ventana, cantidad_visible)-> None:

    for snack in contador_de_snacks:
        contador_de_snacks[snack]=1
        cantidad_visible.config(text=f'{snack} (0)')

    ventana.destroy()

#----------------------------------------------------------------CANCELAR_COMPRA_BOLETOS----------------------------------------------------------#

def cancelar_compra_boletos(comprar_boleto, ventana_principal, entrada) -> None:

    for cantidad in comprar_boleto:
        comprar_boleto[cantidad]=0
        entrada.config(text=f'Cantidad de entradas ({comprar_boleto[cantidad]})')

    ventana_principal.destroy()
    
#boletos = {'disponibles': x, 'totales': y, 'adquiridos': y-x, 'comprando':0}m

#-----------------------------------------------------------------------AUMENTAR_BOLETOS----------------------------------------------------------#

def aumentar_boletos(boletos, comprar_boleto, entrada)-> None:

    for cantidad in comprar_boleto:

        if comprar_boleto[cantidad] < boletos['disponibles']:
            comprar_boleto[cantidad]+=1
            entrada.config(text=f'{comprar_boleto[cantidad]}')

#-----------------------------------------------------------DISMINUIR_BOLETOS---------------------------------------------------------------------#

def disminuir_boletos(comprar_boletos, entrada)-> None:

    for cantidad in comprar_boletos:

        if comprar_boletos[cantidad]>0:
            comprar_boletos[cantidad]-=1
            entrada.config(text=f'{comprar_boletos[cantidad]}')
  
#---------------------------------------------------------------AUMENTAR_SNACKS-------------------------------------------------------------------#

def aumentar_snacks(snack, contador_de_snacks, cantidad_visible)-> None:

    contador_de_snacks[snack]+=1
    cantidad_visible.config(text=f'{snack} ({contador_de_snacks[snack]})')

#----------------------------------------------------------------DISMINUIR_SNACKS-----------------------------------------------------------------#

def disminuir_snacks(snack, contador_de_snacks, cantidad_visible)-> None:

    if contador_de_snacks[snack]>0:
        contador_de_snacks[snack]-=1
        cantidad_visible.config(text=f'{snack} ({contador_de_snacks[snack]})')

#---------------------------------------------------------------------BTN_ACEPTAR/CANCELAR_SNACKS-------------------------------------------------#

def botones_aceptar_cancelar_snacks(ventana3, contador_de_snacks, cantidad_visible)->None:

    aceptar = Button(
                        ventana3, text='Aceptar', 
                        command=lambda: cerrar_ventana(ventana3),
                        fg='blue'
                    )
    aceptar.pack()
    aceptar.place(x=95, y=220)
   
    cancelar = Button(
                        ventana3, text='Cancelar compra', 
                        command=lambda: reiniciar_snacks(contador_de_snacks, ventana3, cantidad_visible),
                        fg='red'
                     )
    cancelar.pack()
    cancelar.place(x=70, y=250)
 
#--------------------------------------------------------------BTN_SNACKS-------------------------------------------------------------------------#

def botones_snacks(ventana3, informacion_snacks, contador_de_snacks)->None:

    for snack in informacion_snacks:
        
        posiciones = Frame(ventana3,bg='black')
        posiciones.pack(side='top', anchor='w')

        cantidad_visible = Label(
                                    posiciones, text=f'{snack} ({contador_de_snacks[snack]})',
                                    width=15, fg='white', bg='black'
                                )
        cantidad_visible.pack(side='left', anchor='w')

        restar = Button(
                            posiciones, text='- 1',
                            command=lambda s=snack, c=cantidad_visible: disminuir_snacks(s, contador_de_snacks, c),
                            fg='red'
                        )
        restar.pack(side='left')

        sumar = Button(
                        posiciones, text='+1',
                        command=lambda s=snack, c=cantidad_visible: aumentar_snacks(s, contador_de_snacks, c),
                        fg='blue'
                      )
        sumar.pack(side='left')

        precios = Label(
                            posiciones, text=f'${informacion_snacks[snack]}',
                            width=12, fg='white', bg='black'
                        )
        precios.pack(side='left')
       

    botones_aceptar_cancelar_snacks(ventana3, contador_de_snacks, cantidad_visible)

#-----------------------------------------------------------------OBTENER_SNACKS------------------------------------------------------------------#

def obtener_snacks(objetivo)-> dict:
    url = "http://vps-3701198-x.dattaweb.com:4000/" + objetivo
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    return response.json() #Retorna una diccionario ya traducido de Json

#------------------------------------------------------------------VENTANA_SNACKS-----------------------------------------------------------------#

def ventana_de_snacks(contador_de_snacks:dict, informacion_snacks:dict)-> None:

    ventana_snacks = Tk()
    ventana_snacks.geometry('250x300')
    ventana_snacks.config(bg='black')
    ventana_snacks.resizable(width=False, height=False)

    encabezado = Label(
                        ventana_snacks, text='COMPRAR SNACKS',
                        fg='white', bg='black'
                      )
    encabezado.pack(side='top')

    botones_snacks(ventana_snacks, informacion_snacks, contador_de_snacks)

    ventana_snacks.mainloop()

#---------------------------------------------------------------SNACK_COMPRADOS-------------------------------------------------------------------#

def snacks_comprados(contador_de_snacks, ventana_final, informacion_snacks, lista_final)-> None:

    for cantidades_snacks in contador_de_snacks:

        cantidades = Frame(ventana_final, bg='black')
        cantidades.pack(side='top', anchor='w')
        
        if contador_de_snacks[cantidades_snacks] > 0:
            
            snacks_seleccionados = Label(
                                            cantidades, text=f'{contador_de_snacks[cantidades_snacks]} {cantidades_snacks}',
                                            font=20,    width=20, fg='orange', bg='black'
                                        )
            snacks_seleccionados.pack(side='left')
          
            precio_snacks_seleccionados = Label(
                                                    cantidades, text= precio_por_snack(cantidades_snacks, contador_de_snacks,
                                                                                       informacion_snacks, lista_final),
                                                    font=20, fg='green', bg='black'
                                                )
            precio_snacks_seleccionados.pack(side='left')

#------------------------------------------------------------BOLETOS_COMPRADOS--------------------------------------------------------------------#

def boletos_comprados(ventana_final, boleto_comprado)-> None:

    tickets = Frame(ventana_final,bg='black')
    tickets.pack(side='top', anchor='w')
  
    cantidad_boletos = Label(
                                tickets, text=f'{boleto_comprado[cantidad]} Entradas', 
                                font=20, width=20, 
                                fg='orange', bg='black'
                            )
    cantidad_boletos.pack(side='left',  anchor='w')

    precio_boletos_seleccionados = Label(
                                            tickets, text=precio_boletos(boleto_comprado),
                                            font=20, fg='green', 
                                            bg='black'
                                        )
    precio_boletos_seleccionados.pack(side='left')
  
#-----------------------------------------------------------------MOSTRAR_PRECIO_FINAL------------------------------------------------------------#

def mostrar_precio_total(ventana_final, lista_final, boleto_comprado)-> None:

    linea_final = Frame(ventana_final, bg='black')
    linea_final.pack(side='top', anchor='w', pady=15)

    palabra_total = Label(
                            linea_final, text='TOTAL',
                            font=20,     width=20, 
                            fg='red',    bg='black'
                        )
    palabra_total.pack(side='left', anchor='w')

    precio_total = Label(
                            linea_final, text=precio_final(lista_final, boleto_comprado),
                            fg='green',  bg='black', font=20
                        )
    precio_total.pack(side='left')

#------------------------------------------------------------------PRECIO_FINAL-------------------------------------------------------------------# 

def precio_final(lista_final, boleto_comprado)-> str:

    boletos: float = float(precio_boletos(boleto_comprado))
    total: int = 0

    for precios in lista_final:
        total+=precios

    return str(total+boletos)

#---------------------------------------------------------------PRECIO_BOLETOS--------------------------------------------------------------------#

def precio_boletos(boleto_comprado)-> str:

    return str(boleto_comprado[cantidad]*PRECIO_DE_ENTRADA)

#----------------------------------------------------------------PRECIO_SNACK---------------------------------------------------------------------#

def precio_por_snack(nombre_snack, cantidad_snack, precio_snack, lista_final)-> str:

    precio_final = cantidad_snack[nombre_snack] * float(precio_snack[nombre_snack])
    lista_final.append(precio_final)

    return str(precio_final)

#--------------------------------------------------------------PANTALLA_RESERVAS------------------------------------------------------------------#

def ventana_de_reservas(ventana2, dict_menu)-> None:

    ventana2.withdraw()
    lista_final: list =[]
    boletos: dict = {'disponibles': 5, 'totales': 10}
    comprar_boleto: dict = {'cantidad': 0}
    informacion_snacks: dict = obtener_snacks(snacks)
    contador_de_snacks: dict = {}
    cantidad_de_snacks(informacion_snacks, contador_de_snacks)

    ventana = Toplevel()
    ventana.geometry('300x150')
    ventana.title('')
    ventana.resizable(width=False, height=False)

    comprar_entradas = Label(ventana, text='SECCION DE RESERVAS')
    comprar_entradas.pack()

    entrada = Label(ventana, text=f'disponibles')
    entrada.pack()
    entrada.place(x=20, y=20)

    opciones_snacks = Button(
                                ventana, text='Añadir snacks', 
                                command=lambda: ventana_de_snacks(contador_de_snacks, informacion_snacks)
                            )
    opciones_snacks.pack()
    opciones_snacks.place(x=60, y=70)

    terminar_compra = Button(
                                ventana, text='Carrito', 
                                command=lambda: ventana_confirmar_compra(informacion_snacks, contador_de_snacks,
                                                                         boletos, comprar_boleto, lista_final, 
                                                                         ventana, ventana2, dict_menu)
                            )
    terminar_compra.pack()
    terminar_compra.place(x=150, y=70)

    restar_cantidad = Button(
                                ventana, text='- 1', 
                                command=lambda: disminuir_boletos(comprar_boleto, entrada)
                            )
    restar_cantidad.pack()

    sumar_cantidad = Button(
                                ventana, text='+1', 
                                command=lambda: aumentar_boletos(boletos, comprar_boleto, entrada)
                           )
    sumar_cantidad.pack()
    sumar_cantidad.place(x=160, y=21)

    cancelar = Button(
                        ventana, text='Cancelar compra', 
                        command=lambda: cancelar_compra_boletos(comprar_boleto, ventana, entrada)
                     )
    cancelar.pack()

#---------------------------------------------------------------OBTENCION_INFO_PELICULA-----------------------------------------------------------#

def api_ventana_secundaria(id_principal):

    guardar: list = []

    url = "http://vps-3701198-x.dattaweb.com:4000/movies/" + id_principal
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    response1 = requests.get(url, headers=headers)

    if response1.status_code == 200:
        x = response1.json() #diccionario

    informacion = list(x.keys())

    for i in range(4,8): 
        variable = x[informacion[i]] 
        guardar.append(variable)   # guardo la informacion que necesito de la pelicula

    return id_principal, guardar

#-------------------------------------------------------------VOLVER_AL_MENU----------------------------------------------------------------------#

def volver_al_menu(ventana_secundaria,ventana_principal) -> None:

    ventana_principal.iconify()
    ventana_principal.deiconify()
    ventana_secundaria.destroy()

#-------------------------------------------------------------------BOTONES-----------------------------------------------------------------------#

def botones (ventana_secundaria,ventana_principal, dict_menu) -> None:

    '''
    BTN-VOLVER AL MENU
        PRE CONDICION: el usuario clickea el boton
        POST CONDICION: al clickear el boton se cerrara la ventana secundaria y se volvera a al menu

    BTN-RESERVAR
        PRE CONDICION: el usuario clickea el boton
        POST CONDICION: al clickear el boton se abrira la ventana de reservar
    '''

    boton_volver_al_menu = Button(
                                    ventana_secundaria,  text= "VOLVER AL MENU", 
                                    background= "black",  fg="gold", 
                                    width= 20,           height= 5, 
                                    command= lambda: volver_al_menu(ventana_secundaria,ventana_principal)
                                  )
    boton_volver_al_menu.place(relx=0.1, rely=0.1, anchor=tk.CENTER)

    boton_reservar = Button(
                                ventana_secundaria,  text= "RESERVAR", 
                                background= "black",  fg="gold",  
                                width= 20,          height= 5,
                                command= lambda: ventana_de_reservas(ventana_secundaria, dict_menu)
                            )
    boton_reservar.place(relx=0.88, rely=0.9, anchor=tk.CENTER)

#-------------------------------------------------------------------SALA--------------------------------------------------------------------------#

def sala(ventana_secundaria, id) -> None:

    sala_proyectar = Label(
                            ventana_secundaria,   text= "SALA  " + id,
                            background= "black",  fg="red",    
                          )
    sala_proyectar.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

#--------------------------------------------------------------------SINOPSIS---------------------------------------------------------------------#

def sinopsis(ventana_secundaria, guardar) -> None: 

    sinopsis = Label(
                        ventana_secundaria, text= "SINOPSIS: ",
                        background= "black", fg="red"  
                    )
    sinopsis.place(relx=0.2, rely=0.3, anchor=tk.CENTER)

    texto_sinopsis = Label(
                            ventana_secundaria,   text= guardar[0],
                            background= "black",  fg="red",    
                            wraplength= 700
                          )
    texto_sinopsis.place(relx=0.5, rely=0.42, anchor=tk.CENTER)

#------------------------------------------------------------------------GENERO-------------------------------------------------------------------#

def genero(ventana_secundaria, guardar) -> None:

    genero = Label(
                    ventana_secundaria,    text= "GENERO: ",
                    background= "black",   fg="red"     
                  )
    genero.place(relx=0.2, rely=0.55, anchor=tk.CENTER)

    texto_genero = Label(
                            ventana_secundaria,    text= guardar[1],
                            background= "black",   fg="red"    
                        )  
    texto_genero.place(relx=0.25, rely=0.55, anchor=tk.CENTER)
    
#----------------------------------------------------------------ACTORES--------------------------------------------------------------------------#

def actores(ventana_secundaria, guardar) -> None:

    actores = Label(
                    ventana_secundaria,     text= "ACTORES: ",
                    background= "black",    fg="red"      
                   )
    actores.place(relx=0.2, rely=0.66, anchor=tk.CENTER)

    texto_actores = Label(
                            ventana_secundaria,     text= guardar[3],
                            background= "black",    fg="red"    
                         )
    texto_actores.place(relx=0.35, rely=0.66, anchor=tk.CENTER)

#-------------------------------------------------------------DURACION----------------------------------------------------------------------------#

def duracion(ventana_secundaria, guardar) -> None:

    duracion = Label(
                        ventana_secundaria,  text= "DURACION: ",
                        background= "black", fg="red" 
                    )
    duracion.place(relx=0.2, rely=0.6, anchor=tk.CENTER)

    texto_duracion = Label(
                            ventana_secundaria,  text= guardar[2],
                            background= "black", fg="red"
                          )
    texto_duracion.place(relx=0.25, rely=0.6, anchor=tk.CENTER)

#----------------------------------------------------------HAY ASIENTOS?--------------------------------------------------------------------------#

def no_hay_lugar():

        mensaje: str = messagebox.showinfo("Lo sentimos, no hay mas asientos disponibles para ver esta pelicula por favor vuelva al menu")

#-----------------------------------------------------------PANTALLA_SECUNDARIA-------------------------------------------------------------------#

def ventana_informacion_pelicula(dict_menu : dict , ventana_principal) -> Toplevel:

    ventana_principal.withdraw()
    id_principal = dict_menu["id"]
    id, guardar = api_ventana_secundaria(id_principal)

    ventana_secundaria = Toplevel()
    ventana_secundaria.title("ventana secundaria")
    ventana_secundaria.geometry("1350x700")
    ventana_secundaria.config(background="black")
   
    botones(ventana_secundaria,ventana_principal,dict_menu)
    sala(ventana_secundaria, id)
    sinopsis(ventana_secundaria, guardar)
    genero(ventana_secundaria, guardar)
    actores(ventana_secundaria, guardar)
    duracion(ventana_secundaria,guardar)
    ventana_secundaria.mainloop()

    return ventana_secundaria

#-------------------------------------------------------------OBTENCION_PELICULA_CINE-------------------------------------------------------------#

def boton_peliculas(sub_id : int,ventana,id_cine,nombre_cine) -> None:

    url = "http://vps-3701198-x.dattaweb.com:4000/movies/" + str(sub_id)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    response__1 = requests.get(url, headers=headers)

    if response__1.status_code == 200:
        
        archivo = response__1.json() #diccionario
        id = archivo["id"]
        nombre = archivo["name"]
        diccionario : dict = {"name": nombre,"id": id , "cinema_id": id_cine,"location": nombre_cine}
        print(diccionario)
        ventana_informacion_pelicula(diccionario,ventana)
    
#--------------------------------------------------------------------POSTERS----------------------------------------------------------------------#

def lista_posters(sub_lista : str)-> str:

    url = "http://vps-3701198-x.dattaweb.com:4000/posters/" + str(sub_lista)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    response__1 = requests.get(url, headers=headers)

    if response__1.status_code == 200:
        datos = response__1.json() #diccionario
       
        for i in datos:
            variable = datos[i]

            return variable
    
#--------------------------------------------------------------------ID_DE_PELICULAS--------------------------------------------------------------#

def lista_peliculas(sub_lista : list, id : str)-> list:
    
    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas/{0}/movies".format(id)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    response__1 = requests.get(url, headers=headers)

    if response__1.status_code == 200:
        datos = response__1.json() #diccionario
        
        for i in datos:
            variable = i["has_movies"]
            sub_lista += variable

    print(sub_lista)

    return sub_lista

#---------------------------------------------------------------BUSCAR_PELICULAS------------------------------------------------------------------#

def buscar(cajon, ventana, sub_lista_de_peliculas,id_cinema,nombre_locacion) -> None:

    datos = cajon.get().upper()

    lista_de_peliculas : list = []
    lista_completa : list = []
    
    for vueltas in sub_lista_de_peliculas:
        url = "http://vps-3701198-x.dattaweb.com:4000/movies/{0}".format(vueltas)
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

        headers = {'Authorization': f'Bearer {token}'} #llave de acceso
        response__1 = requests.get(url, headers=headers)

        if response__1.status_code == 200:
            archivo = response__1.json()
            lista_de_peliculas.append(archivo["name"])
            lista_completa.append(archivo) 

    if datos in lista_de_peliculas:

        for sub_vueltas in lista_completa:

            if datos == sub_vueltas["name"]:

                id = sub_vueltas["id"]
                diccionario : dict = {"name" : datos ,"id" : id , "cinema_id": id_cinema,"location": nombre_locacion}

                print(diccionario)
                ventana_informacion_pelicula(diccionario,ventana)
    else:
        sub_ventana = Toplevel()
        sub_ventana.geometry("300x200")
        sub_ventana.title("ERROR !!!")

        sub_frame = Frame(sub_ventana,bg="black")
        sub_frame.pack(expand=True,fill="both")

        mensaje = Label(
                         sub_frame, text="NO SE ENCONTRO LA PELICULA. INTENTE DE NUEVO",
                         bg="black",fg="red"
                        )
        mensaje.pack(ipadx=50,ipady=50)

        sub_boton = Button(
                            sub_frame, text = "OK",
                            command=sub_ventana.destroy, 
                            bg="black",fg="red"
                          )
        sub_boton.pack(ipadx=25,ipady=10)

#-----------------------------------------------------------BOTON_SELECCION_PELICULA--------------------------------------------------------------#

def crear_boton_pelicula(numero_id,nombre_cine,sub_frame, imagen, pelicula_info, ventana, row, column) -> None:

    boton_pelicula = Button(
                              sub_frame, image=imagen, bg="black",
                              command=lambda info=pelicula_info:  boton_peliculas(info, ventana,numero_id,nombre_cine)
                            )
    boton_pelicula.grid(row=row, column=column)

#-----------------------------------------------------------BASE64_POSTERS------------------------------------------------------------------------#

def cargar_imagen_pelicula(pelicula_info):

    funcion_pelicula: str = lista_posters(pelicula_info) 
    base64_data_pelicula: str = funcion_pelicula.split(",")[1]  
    imagen_a_deco_pelicula: bytes = base64.b64decode(base64_data_pelicula)
    imagen_capturada_pelicula = ImageTk.PhotoImage(data=imagen_a_deco_pelicula)

    return imagen_capturada_pelicula  

#--------------------------------------------------------------SCROLLBAR_VENTANA_PRINCIPAL--------------------------------------------------------#

def configurar_frame_canvas_scrollbar(ventana:None, side:str)-> tuple:

    frame = Frame(
                   ventana,     bg="black",
                   height=1000, width=600,
                   relief="raised", bd=25
                 )
    frame.pack(side=side, fill="both", expand=True)

    canvas = Canvas(frame, bg="black")
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(frame, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.config(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    sub_frame = Frame(canvas, bg="black")
    canvas.create_window((0, 0), window=sub_frame, anchor="nw")

    return sub_frame

#--------------------------------------------------------------VISUALIZAR_POSTER------------------------------------------------------------------#

def ejecucion_boton_pelicula(listas_de_peliculas, ventana,cine_numero,nombre_cine):

    sub_frame_1: tuple = configurar_frame_canvas_scrollbar(ventana, "left")
    sub_frame_2: tuple = configurar_frame_canvas_scrollbar(ventana, "right")
    
    lista_imagenes: list = []

    corte : int = len(listas_de_peliculas) // 2

    for i in range(len(listas_de_peliculas)):
        pelicula_info = listas_de_peliculas[i]
        
        imagen_pelicula = cargar_imagen_pelicula(pelicula_info)
        lista_imagenes.append(imagen_pelicula)
        if i < corte:
            sub_frame = sub_frame_1
        else:
            sub_frame = sub_frame_2

        crear_boton_pelicula(  cine_numero, nombre_cine, sub_frame, 
                               imagen_pelicula, pelicula_info, ventana,
                               row=i // 3, column=i % 3
                            )
    
    return lista_imagenes

#--------------------------------------------------------------VENTANA_PRINCIPAL------------------------------------------------------------------#

def ventana_principal(numero_cine,nombre_cine,vent):
    
    vent.destroy()

    ventana = Tk()
    ventana.geometry("1600x720")
    ventana.title("TOTEM CINEMA")

    fram_1 = Frame(ventana, bg="black", relief="raised", bd=25)
    fram_1.pack(fill="x")

    cajon = Entry(fram_1)
    cajon.grid(row=0, column=0, ipadx=100, ipady=5)

    listas_de_peliculas: list = lista_peliculas([],numero_cine)

    boton_busqueda = Button(
                             fram_1, text="BUSCAR",
                             command=lambda: buscar(cajon, ventana, listas_de_peliculas,numero_cine,nombre_cine) ,
                             bg="black", fg="red"
                            )
    boton_busqueda.grid(row=0, column=1, padx=270, ipadx=30, ipady=5)

    ubicacion = Label(
                        fram_1, text=f"CINE : {nombre_cine}",
                        bg="black", fg="red"
                     )
    ubicacion.grid(row=0, column=2, padx=100, ipadx=30, ipady=5)

    imagen_ejecutable: list = ejecucion_boton_pelicula(listas_de_peliculas, ventana, numero_cine, nombre_cine)

    ventana.mainloop()

#----------------------------------------------------------BOTONES_ELEGIR_CINES-------------------------------------------------------------------#

def crear_boton_cines(frame, cine_id, nombre_cine, ventana) -> None:

    boton_1 = Button(
                        frame, text=nombre_cine, 
                        command=lambda : ventana_principal(cine_id,nombre_cine,ventana),
                        bg="black",fg="red"
                    ) 
    boton_1.pack(ipadx=20,ipady=5,pady=5)

#-------------------------------------------------------------OBTENER_CINES-----------------------------------------------------------------------#

def cinemas(lista_id : list , nombre_cine : list):

    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas"

    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso

    response__1 = requests.get(url, headers=headers)

    if response__1.status_code == 200:
        datos = response__1.json() #diccionario

        for i in datos:
            lista_id.append(i["cinema_id"])
            nombre_cine.append(i["location"])

    return lista_id , nombre_cine

#------------------------------------------------------------VENTANA_ELEGIR_CINE------------------------------------------------------------------#

def ventana0():

    ventana = Tk()
    ventana.geometry("600x400")
    ventana.title("MENU")

    frame = Frame(ventana, bg="black")
    frame.pack(expand=True, fill="both")

    cine_id,nombre_cine = cinemas([],[])
    print(cine_id)
    print(nombre_cine)
    numero : int = 0

    for vueltas in range(len(cine_id)):
        crear_boton_cines(frame,cine_id[numero],nombre_cine[numero],ventana)
        numero += 1
    
    ventana.mainloop()
    
#----------------------------------------------------------------------APP_QR---------------------------------------------------------------------#
#--------------------------------------------------------------CREAR_QR_GUARDAR_EN_PDF------------------------------------------------------------#

def crear_qr(boleto_comprado, dict_menu, ventana_final, ventana3, ventana2, contador_de_snacks) -> None:

    ruta_qr: str = os.path.join(os.getcwd(), 'QR')

    if not os.path.exists(ruta_qr):
        os.makedirs(ruta_qr)

    archivos_en_qr: list[str] = os.listdir(ruta_qr)
    cantidad_de_archivos: int = len(archivos_en_qr)

    id_qr: str = 'QR_' + str(cantidad_de_archivos + 1)
    pelicula = dict_menu['name']
    cine = dict_menu['location']
    entradas: str = str(boleto_comprado['cantidad'])
    tiempo: str = fecha_y_hora()

    contenido_qr: str = f'{id_qr}, {pelicula}, {cine}, {entradas} entradas, {tiempo}'
    ruta_imagen_qr: str = os.path.join(ruta_qr, f'{id_qr}.png')
    ruta_pdf: str = os.path.join(ruta_qr, f'{id_qr}.pdf')

    # Guardar la imagen QR
    img = qrcode.make(contenido_qr)
    img.save(ruta_imagen_qr)

    # Crear el archivo PDF
    c = canvas.Canvas(ruta_pdf, pagesize=letter)

    # Agregar la imagen QR al PDF
    c.drawInlineImage(ruta_imagen_qr, 100, 500, width=300, height=300)

    # Cerrar el archivo PDF
    c.save()

    # Limpiar después de guardar
    os.remove(ruta_imagen_qr)

    boleto_comprado['cantidad'] = 0

    for snack in contador_de_snacks:
        contador_de_snacks[snack] = 0

    ventana_final.destroy()
    ventana2.deiconify()

#-------------------------------------------------------------FECHA_Y_HORA_QR---------------------------------------------------------------------#

def fecha_y_hora() -> str:

    from time import localtime, strftime
    estructura = localtime()

    return strftime('%Y-%m-%d %H:%M:%S', estructura)

#-------------------------------------------------------------------IMAGEN_DESDE_PDF--------------------------------------------------------------#

def extraer_imagen_desde_pdf(archivo_pdf, ruta_imagen_png) -> bool:

    try:
        with fitz.open(archivo_pdf) as pdf_doc:

            for pagina_num in range(pdf_doc.page_count):
                pagina = pdf_doc[pagina_num]
                imagen = pagina.get_pixmap()
                imagen.save(ruta_imagen_png)

        print(f"Imagen extraída del PDF y guardada en {ruta_imagen_png}")
        return True

    except Exception as e:
        print(f"Error al extraer la imagen del PDF: {str(e)}")
        return False

#---------------------------------------------------------------DECODIFICANDO_QR_DESDE_IMAGEN-----------------------------------------------------#

def decodificar_qr_desde_imagen(ruta_imagen) -> None:

    imagen = Image.open(ruta_imagen)
    datos_qr: list = decode(imagen)

    if datos_qr:
        return datos_qr[0].data.decode('utf-8')
    else:
        return None

#-----------------------------------------------------------AGREGAR/VERIFICAR_QR_EN_TXT-----------------------------------------------------------#

def agregar_a_ingresos_txt(codigo_qr) -> None:

    # Verificar si el código QR ya está en ingresos.txt
    with open("ingresos.txt", "r") as archivo_ingresos:
        lineas: list[str] = archivo_ingresos.readlines()

        if codigo_qr not in lineas:
            # Agregar el código QR solo si no está repetido
            with open("ingresos.txt", "a") as archivo_ingresos:
                archivo_ingresos.write(f'{codigo_qr}\n')
                print(f"Código QR agregado a ingresos.txt: {codigo_qr}")
        else:
            print(f"El código QR ya está en ingresos.txt: {codigo_qr}")

#--------------------------------------------------------------------QR_PDF-----------------------------------------------------------------------#

def codigo(cajon, ventana, carpeta_pdf) -> None:

    dato_entrada = cajon.get().upper()
    print(f"Ingresaste: {dato_entrada}")

    archivo_pdf: str = f"{dato_entrada}.pdf"
    ruta_completa_pdf: str = os.path.join(carpeta_pdf, archivo_pdf)

    if os.path.exists(ruta_completa_pdf):
        print(f"El archivo {archivo_pdf} existe.")

        # Ruta para guardar la imagen extraída
        ruta_imagen_png: str = os.path.join(carpeta_pdf, f'{dato_entrada}.png')

        # Obtener el contenido del PDF como imagen PNG
        if extraer_imagen_desde_pdf(ruta_completa_pdf, ruta_imagen_png):
            print(f"Imagen extraída correctamente del PDF {archivo_pdf}")

            # Decodificar el código QR desde la imagen
            codigo_qr = decodificar_qr_desde_imagen(ruta_imagen_png)

            if codigo_qr is not None:
                print(f"Código QR extraído: {codigo_qr}")
                agregar_a_ingresos_txt(codigo_qr)

            else:
                print("No se encontró código QR en la imagen.")
        else:
            print(f"No se pudo extraer la imagen del PDF {archivo_pdf}")

    else:
        print(f"El archivo {archivo_pdf} no existe.")

    if os.path.exists(ruta_imagen_png):
        os.remove(ruta_imagen_png) # Eliminar la imagen PNG después de leer el código QR
        print(f"Imagen PNG eliminada: {ruta_imagen_png}")
    else:
        print(f"No se encontró la imagen PNG para eliminar: {ruta_imagen_png}")

    # No cerrar la ventana de Tkinter

#------------------------------------------------------------------LECTURA_QR---------------------------------------------------------------------#

def lectura_qr(ventana_qr) -> None:

    camara = cv2.VideoCapture(0)
    ciclo: bool = True
    dato_qr: str = ""

    while ciclo:
        ret, frame = camara.read()

        if cv2.waitKey(1) & 0xFF == ord("s"):
            ciclo = False

        detector = cv2.QRCodeDetector()
        data, bbox, rectifiedImage = detector.detectAndDecode(frame)

        if len(data) > 0:
            cv2.imshow("web", rectifiedImage)
            dato_qr = data
            ciclo = False
        else:
            cv2.imshow("web", frame)

    camara.release()
    cv2.destroyAllWindows()

    print(dato_qr)

    with open("ingresos.txt", "r") as archivo_lectura:
        contenido_actual: str = archivo_lectura.read()

    if opcion_de_cinema in dato_qr and dato_qr not in contenido_actual:
        with open("ingresos.txt", "a") as archivo:
            archivo.write(dato_qr + '\n')
        ventana_qr.destroy()

    elif dato_qr in contenido_actual:
        ventana_error = Toplevel()
        ventana_error.geometry("300x200")
        ventana_error.title("ERROR !!!")

        frame_error = Frame(ventana_error, bg="black")
        frame_error.pack(expand=True, fill="both")

        mensaje = Label(
                          frame_error, text="CÓDIGO YA REGISTRADO",
                          bg="black", fg="red"
                        )
        mensaje.pack(ipadx=50, ipady=50)

        boton_error = Button(
                              frame_error,        text="OK",
                              background="black", fg="red",
                              command=ventana_error.destroy
                            )
        boton_error.pack(ipadx=25, ipady=10)
    else:
        ventana_error = Toplevel()
        ventana_error.geometry("300x200")
        ventana_error.title("ERROR !!!")

        frame_error = Frame(ventana_error, bg="black")
        frame_error.pack(expand=True, fill="both")

        mensaje = Label(
                          frame_error, text="CÓDIGO INVALIDO",
                          bg="black",  fg="red"
                        )
        mensaje.pack(ipadx=50, ipady=50)

        boton_error = Button(
                              frame_error,        text="OK",
                              background="black", fg="red",
                              command=ventana_error.destroy
                            )
        boton_error.pack(ipadx=25, ipady=10)

#------------------------------------------------------------MENU_APP_QR-------------------------------------------------------------------------#

def menu_QR() -> None:

    ventana_menu_qr = tk.Tk()
    ventana_menu_qr.geometry("500x500")
    ventana_menu_qr.title("Validacion")

    frame_principal = Frame(ventana_menu_qr, bg="black")
    frame_principal.pack(expand=True, fill="both")

    label_ingrese_codigo = Label(
                                  frame_principal,    text="INGRESE SU CODIGO",
                                  background="black", fg="red"
                                )
    label_ingrese_codigo.pack(pady=20, ipadx=50, ipady=20)

    cajon = Entry(frame_principal)
    cajon.pack(pady=20, ipadx=50)

    btn_validar_qr = Button(
                             frame_principal,    text="VALIDAR",
                             background="black", fg="red",
                             command=lambda: codigo(cajon, ventana_menu_qr, "QR")
                            )
    btn_validar_qr.pack(pady=20, ipadx=50, ipady=5)

    btn_encender_qr = Button(
                             frame_principal,    text="ENCENDER QR",
                             background="black", fg="red",
                             command=lambda: lectura_qr(ventana_menu_qr)
                            )
    btn_encender_qr.pack(pady=20, ipadx=50, ipady=5)

#------------------------------------------------------------MENU/OPCION-------------------------------------------------------------------------#

def menu() -> str:

    print('MENU DEL CINE')
    print()
    print('1) APP CINE')
    print('2) App QR')
    print('3) Salir del menú')
    print()

    return str(input('Elija opción: '))

#-------------------------------------------------------------------MAIN-------------------------------------------------------------------------#

def main():

    sigamos: bool = True

    while sigamos:
        respuesta: str = menu()

        if respuesta == '1':
            ventana0()
        elif respuesta == '2':
            menu_QR()
        elif respuesta == '3':
            sigamos: bool = False

main()
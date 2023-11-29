from tkinter import Tk, Label, Button, Frame, Entry, Toplevel, Canvas, Scrollbar, messagebox, CENTER
from PIL import ImageTk
from base64 import b64decode
from requests import get
from cv2 import imread, cvtColor, QRCodeDetector, COLOR_BGR2GRAY, waitKey, imshow, VideoCapture, destroyAllWindows
from qrcode import make
from time import localtime, strftime
from os import path, getcwd, makedirs, listdir, remove
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import fitz

letra_español:str = 'Ñ'
conversion_de_letra:str = 'NI'
ruta_ingresos:str = 'ingresos.txt'
PRECIO_DE_ENTRADA:int=1800.00

def obtener_cantidad_asientos(dict_menu:dict)->int:

    
    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == 200:
        lista_de_cinemas = verificar_archivo.json()

        for informacion_cinemas in lista_de_cinemas:
            if informacion_cinemas['location'] == dict_menu['location']:
                return informacion_cinemas['available_seats'] 
  
#--------------------------------------------------------------------CERRAR_VENTANA---------------------------------------------------------------#

def cerrar_ventana(ventana, ventana_reserva)-> None:

    ventana.destroy()
    ventana_reserva.deiconify()


def mostrar_encabezados(ventana_final, dict_menu)->None:

    name = 'name'
    encabezado = Label(
                            ventana_final, text=f'CARRITO PARA:', 
                            font=20, fg='white', bg='black'
                        )
    encabezado.pack(side='top', pady=5)

    nombre_pelicula = Label(ventana_final, text=f'{dict_menu[name]}', font=20, fg='white', bg='black')
    nombre_pelicula.pack(pady=10)


def botones_pantalla_final(ventana_final, ventana_principal, cantidad_entradas, dict_menu, 
                            ventana3, contador_de_snacks)->None:

    botones_de_accion = Frame(ventana_final,bg='black')
    botones_de_accion.pack(side='top', anchor='center', pady=10)
    
    boton_comprar = Button(
                                botones_de_accion, text='PAGAR', 
                                command=lambda: crear_qr(cantidad_entradas, dict_menu, ventana_final,
                                                         ventana3, ventana_principal, contador_de_snacks)
                            )
    boton_comprar.pack(side='top', anchor='n', pady=10)

    boton_cancelar_compra = Button(
                                    botones_de_accion, text='CANCELAR', command=lambda: cancelar_compra(ventana3, ventana_final)
                                    )
    boton_cancelar_compra.pack(side='bottom', anchor='center') 

#--------------------------------------------------------------CONFIRMAR_COMPRA-------------------------------------------------------------------#

def ventana_confirmar_compra( informacion_snacks, contador_de_snacks, asientos_disponibles_en_la_sala,
                              lista_final, ventana3,
                              dict_menu, eleccion_entradas, ventana_principal)-> None:
    
    name = 'name'
    cantidad_entradas = eleccion_entradas.get()

    if cantidad_entradas == '0' or cantidad_entradas == '':
        ventana3.withdraw()
        messagebox.showwarning('Advertencia', 'No hay boletos seleccionados')
        ventana3.deiconify()
    
    elif int(cantidad_entradas) > asientos_disponibles_en_la_sala:
        ventana3.withdraw()
        messagebox.showwarning('Advertencia', f'No puedes comprar más de {asientos_disponibles_en_la_sala} asientos')
        ventana3.deiconify()

    else:
        ventana3.withdraw()

        ventana_final = Toplevel()
        ventana_final.geometry('352x400')
        ventana_final.config(bg='black')
        ventana_final.resizable(width=False, height=False)

        mostrar_encabezados(ventana_final, dict_menu)        
        snacks_comprados(contador_de_snacks, ventana_final, informacion_snacks, lista_final)
        boletos_comprados(ventana_final, cantidad_entradas)
        mostrar_precio_total(ventana_final, lista_final, cantidad_entradas)
        botones_pantalla_final(ventana_final, ventana_principal, cantidad_entradas, dict_menu, ventana3, contador_de_snacks) 

        ventana_final.mainloop()

#--------------------------------------------------------------CANTIDAD_SNACKS--------------------------------------------------------------------#

def cantidad_de_snacks(informacion_snacks:dict, contador_de_snacks:dict)-> None:

    for snack in informacion_snacks:
        contador_de_snacks[snack]=0

#------------------------------------------------------------------REINICIAR_SNACKS---------------------------------------------------------------#

def reiniciar_snacks(contador_de_snacks:dict, ventana, cantidad_visible:dict, ventana_reserva) -> None:

    for snack in contador_de_snacks:
        contador_de_snacks[snack]=0
        cantidad_visible.config(text=f'{snack}: 0')

    ventana.destroy()
    ventana_reserva.deiconify()

#----------------------------------------------------------------CANCELAR_COMPRA_BOLETOS----------------------------------------------------------#

def cancelar_compra(ventana_anterior, ventana_actual) -> None:

    ventana_actual.destroy()
    ventana_anterior.deiconify()

#---------------------------------------------------------------AUMENTAR_SNACKS-------------------------------------------------------------------#

def aumentar_snacks(snack, contador_de_snacks:dict, cantidad_visible:str) -> None:

    contador_de_snacks[snack]+=1
    cantidad_visible.config(text=f'{snack}: {contador_de_snacks[snack]}')

#----------------------------------------------------------------DISMINUIR_SNACKS-----------------------------------------------------------------#

def disminuir_snacks(snack, contador_de_snacks:dict, cantidad_visible:str) -> None:

    if contador_de_snacks[snack]>0:
        contador_de_snacks[snack]-=1
        cantidad_visible.config(text=f'{snack}: {contador_de_snacks[snack]}')

#---------------------------------------------------------------------BTN_ACEPTAR/CANCELAR_SNACKS-------------------------------------------------#

def botones_aceptar_cancelar_snacks(ventana3, contador_de_snacks:dict, cantidad_visible:str, ventana_reserva)->None:

    aceptar = Button(
                     ventana3, text='Aceptar', 
                     command=lambda: cerrar_ventana(ventana3, ventana_reserva),
                     fg='blue'
                    )
    aceptar.pack()
    aceptar.place(x=95, y=220)
   
    cancelar = Button(
                      ventana3, text='Cancelar compra', 
                      command=lambda: reiniciar_snacks(contador_de_snacks, ventana3, cantidad_visible, ventana_reserva),
                      fg='red'
                     )
    cancelar.pack()
    cancelar.place(x=70, y=250)
 
#--------------------------------------------------------------BTN_SNACKS-------------------------------------------------------------------------#

def botones_snacks(ventana3, informacion_snacks:dict, contador_de_snacks:dict, ventana_reserva, ventana_snacks)->None:

    encabezado = Label(
                        ventana_snacks, text='COMPRAR SNACKS',
                        fg='white', bg='black'
                      )
    encabezado.pack(side='top')

    for snack in informacion_snacks:
        
        posiciones = Frame(ventana3,bg='black')
        posiciones.pack(side='top', anchor='w')

        cantidad_visible = Label(
                                 posiciones, text=f'{snack}: {contador_de_snacks[snack]}',
                                 width=15, fg='white', bg='black'
                                 )
        cantidad_visible.pack(side='left', 
                              anchor='w')

        restar = Button(posiciones, text='- 1', command=lambda s=snack, c=cantidad_visible: 
                        disminuir_snacks(s, contador_de_snacks, c), fg='red')
        restar.pack(side='left')

        sumar = Button(posiciones, text='+1', command=lambda s=snack, c=cantidad_visible: 
                       aumentar_snacks(s, contador_de_snacks, c), fg='blue')
        sumar.pack(side='left')

        precios = Label(posiciones, text=f'${informacion_snacks[snack]}',
                        width=12, fg='white', bg='black')
        precios.pack(side='left')
       

    botones_aceptar_cancelar_snacks(ventana3, contador_de_snacks, cantidad_visible, ventana_reserva)

#-----------------------------------------------------------------OBTENER_SNACKS------------------------------------------------------------------#

def obtener_snacks()-> dict:
    url = "http://vps-3701198-x.dattaweb.com:4000/snacks"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == 200:
        diccionario_snacks = verificar_archivo.json()

    return diccionario_snacks #Retorna una diccionario ya traducido de Json

#------------------------------------------------------------------VENTANA_SNACKS-----------------------------------------------------------------#

def ventana_de_snacks(contador_de_snacks:dict, informacion_snacks:dict, ventana_reserva)-> None:

    ventana_reserva.withdraw()

    ventana_snacks = Toplevel()
    ventana_snacks.geometry('250x300')
    ventana_snacks.config(bg='black')
    ventana_snacks.resizable(width=False, height=False)

    botones_snacks(ventana_snacks, informacion_snacks, contador_de_snacks, ventana_reserva, ventana_snacks)

    ventana_snacks.mainloop()

#---------------------------------------------------------------SNACK_COMPRADOS-------------------------------------------------------------------#

def snacks_comprados(contador_de_snacks:dict, ventana_final, informacion_snacks:dict, lista_final:list[int])-> None:

    for nombre_snacks in contador_de_snacks:

        cantidades = Frame(ventana_final, bg='black')
        cantidades.pack(side='top', anchor='w')
        
        if contador_de_snacks[nombre_snacks] > 0:
            
            snacks_seleccionados = Label(
                                            cantidades, text=f'{contador_de_snacks[nombre_snacks]} {nombre_snacks}',
                                            font=20,    width=25, fg='orange', bg='black'
                                        )
            snacks_seleccionados.pack(side='left')
          
            precio_snacks_seleccionados = Label(
                                                    cantidades, text= precio_por_snack(nombre_snacks, contador_de_snacks,
                                                                                       informacion_snacks, lista_final),
                                                    font=20, fg='green', bg='black'
                                                )
            precio_snacks_seleccionados.pack(side='left')

#------------------------------------------------------------BOLETOS_COMPRADOS--------------------------------------------------------------------#

def boletos_comprados(ventana_final, boleto_comprado)-> None:

    tickets = Frame(ventana_final,bg='black')
    tickets.pack(side='top', anchor='w')
  
    cantidad_boletos = Label(
                                tickets, text=f'{boleto_comprado} Entradas', 
                                font=20, width=25, 
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
                            font=20,     width=25, 
                            fg='red',    bg='black'
                        )
    palabra_total.pack(side='left', anchor='w')

    precio_total = Label(
                            linea_final, text=precio_final(lista_final, boleto_comprado),
                            fg='green',  bg='black', font=20
                        )
    precio_total.pack(side='left')

#------------------------------------------------------------------PRECIO_FINAL-------------------------------------------------------------------# 

def precio_final(lista_final:list[int], cantidad_entradas:str)-> str:

    boletos: float = float(precio_boletos(cantidad_entradas))
    total: int = 0

    for precios in lista_final:
        total+=precios

    return str(total+boletos)

#---------------------------------------------------------------PRECIO_BOLETOS--------------------------------------------------------------------#

def precio_boletos(cantidad_entradas:str) -> str:

    return str(int(cantidad_entradas)*PRECIO_DE_ENTRADA)

#----------------------------------------------------------------PRECIO_SNACK---------------------------------------------------------------------#

def precio_por_snack(nombre_snack, cantidad_snack:dict, precio_snack:dict, lista_final:list[int])-> str:

    precio_final = cantidad_snack[nombre_snack] * float(precio_snack[nombre_snack])
    lista_final.append(precio_final)

    return str(precio_final)

def validar_texto(nuevo_valor:str)->bool:
    return nuevo_valor.isdigit() or nuevo_valor == ''


def presentar_cant_entradas(asientos_disponibles_en_la_sala)->str:
    return f'''Hay {asientos_disponibles_en_la_sala} asientos disponibles
Cantidad de entradas a comprar:'''


def mostrar_cantidad_de_asientos_disponibles(ventana_reserva, asientos_disponibles_en_la_sala:int)->None:

    comprar_entradas = Label(ventana_reserva, text='SECCION DE RESERVAS', fg='white', bg='black')
    comprar_entradas.pack()

    mostrar_cant_asientos = Label(ventana_reserva, 
                                    text= presentar_cant_entradas(asientos_disponibles_en_la_sala), fg='white', bg='black')
    mostrar_cant_asientos.pack()


def textos_y_botones(ventana_reserva, contador_de_snacks:dict, informacion_snacks:dict, lista_final:list[int],
                     asientos_disponibles_en_la_sala:str, dict_menu:dict, ventana2)->None:
    
    validar_ingreso = (ventana_reserva.register(validar_texto), '%P')
    eleccion_entradas = Entry(ventana_reserva, width=5, validate="key", validatecommand=validar_ingreso)
    eleccion_entradas.pack()

    opciones_snacks = Button(
                                ventana_reserva, text='Añadir snacks', 
                                command=lambda: ventana_de_snacks(contador_de_snacks, informacion_snacks, ventana_reserva), 
                                fg='white', bg='black'
                            )
    opciones_snacks.pack()

    terminar_compra = Button(
                                ventana_reserva, text='Carrito', 
                                command=lambda: ventana_confirmar_compra(informacion_snacks, contador_de_snacks,
                                                                        asientos_disponibles_en_la_sala, lista_final, 
                                                                        ventana_reserva, dict_menu, eleccion_entradas, ventana_principal)
                            )  #implememtar lógica para comprar entradas
    terminar_compra.pack()

    cancelar = Button(
                        ventana_reserva, text='Cancelar compra', 
                        command=lambda: cancelar_compra(ventana2, ventana_reserva)
                    )
    cancelar.pack()
    
#--------------------------------------------------------------PANTALLA_RESERVAS------------------------------------------------------------------#

def ventana_de_reservas(ventana2, dict_menu:dict, asientos_disponibles_en_la_sala:str, ventana_principal)-> None:

    if asientos_disponibles_en_la_sala == 0:
        ventana2.withdraw()
        messagebox.showwarning('Advertencia', 'Ya no hay asientos disponibles')
        ventana2.deiconify()

    else:
        ventana2.withdraw()
        lista_final: list =[]
        informacion_snacks: dict = obtener_snacks()
        contador_de_snacks: dict = {}
        cantidad_de_snacks(informacion_snacks, contador_de_snacks)

        ventana_reserva = Toplevel()
        ventana_reserva.geometry('300x160')
        ventana_reserva.title('')
        ventana_reserva.resizable(width=False, height=False)
        ventana_reserva.config(bg='black')

        mostrar_cantidad_de_asientos_disponibles(ventana_reserva, asientos_disponibles_en_la_sala)
        textos_y_botones(ventana_reserva, contador_de_snacks, informacion_snacks, lista_final,
                         asientos_disponibles_en_la_sala, dict_menu, ventana2)

#---------------------------------------------------------------OBTENCION_INFO_PELICULA-----------------------------------------------------------#

def api_ventana_secundaria(id_principal)->tuple:

    guardar: list = []

    url = "http://vps-3701198-x.dattaweb.com:4000/movies/" + id_principal
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == 200:
        x = verificar_archivo.json() #diccionario

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

def botones (ventana_secundaria, ventana_principal, dict_menu:dict, asientos_disponibles_en_la_sala:str) -> None:

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
    boton_volver_al_menu.place(relx=0.1, rely=0.1, anchor=CENTER)

    boton_reservar = Button(
                                ventana_secundaria,  text= "RESERVAR", 
                                background= "black",  fg="gold",  
                                width= 20,          height= 5,
                                command= lambda: ventana_de_reservas(ventana_secundaria, dict_menu, asientos_disponibles_en_la_sala, ventana_principal)
                            )
    boton_reservar.place(relx=0.88, rely=0.9, anchor=CENTER)

#-------------------------------------------------------------------SALA--------------------------------------------------------------------------#

def sala(ventana_secundaria, id) -> None:

    sala_proyectar = Label(
                            ventana_secundaria,   text= "SALA  " + id,
                            background= "black",  fg="red",    
                          )
    sala_proyectar.place(relx=0.5, rely=0.1, anchor=CENTER)

#--------------------------------------------------------------------SINOPSIS---------------------------------------------------------------------#

def sinopsis(ventana_secundaria, guardar) -> None: 

    sinopsis = Label(
                        ventana_secundaria, text= "SINOPSIS: ",
                        background= "black", fg="red"  
                    )
    sinopsis.place(relx=0.2, rely=0.3, anchor=CENTER)

    texto_sinopsis = Label(
                            ventana_secundaria,   text= guardar[0],
                            background= "black",  fg="red",    
                            wraplength= 700
                          )
    texto_sinopsis.place(relx=0.5, rely=0.42, anchor=CENTER)

#------------------------------------------------------------------------GENERO-------------------------------------------------------------------#

def genero(ventana_secundaria, guardar) -> None:

    genero = Label(
                    ventana_secundaria,    text= "GENERO: ",
                    background= "black",   fg="red"     
                  )
    genero.place(relx=0.2, rely=0.55, anchor=CENTER)

    texto_genero = Label(
                            ventana_secundaria,    text= guardar[1],
                            background= "black",   fg="red"    
                        )  
    texto_genero.place(relx=0.25, rely=0.55, anchor=CENTER)
    
#----------------------------------------------------------------ACTORES--------------------------------------------------------------------------#

def actores(ventana_secundaria, guardar) -> None:

    actores = Label(
                    ventana_secundaria,     text= "ACTORES: ",
                    background= "black",    fg="red"      
                   )
    actores.place(relx=0.2, rely=0.66, anchor=CENTER)

    texto_actores = Label(
                            ventana_secundaria,     text= guardar[3],
                            background= "black",    fg="red"    
                         )
    texto_actores.place(relx=0.35, rely=0.66, anchor=CENTER)

#-------------------------------------------------------------DURACION----------------------------------------------------------------------------#

def duracion(ventana_secundaria, guardar) -> None:

    duracion = Label(
                        ventana_secundaria,  text= "DURACION: ",
                        background= "black", fg="red" 
                    )
    duracion.place(relx=0.2, rely=0.6, anchor=CENTER)

    texto_duracion = Label(
                            ventana_secundaria,  text= guardar[2],
                            background= "black", fg="red"
                          )
    texto_duracion.place(relx=0.25, rely=0.6, anchor=CENTER)

#----------------------------------------------------------HAY ASIENTOS?--------------------------------------------------------------------------#

def no_hay_lugar():

        mensaje: str = messagebox.showinfo("Lo sentimos, no hay mas asientos disponibles para ver esta pelicula por favor vuelva al menu")

def saber_asientos_comprados()->dict:
    
    informacion_asientos_comprados:dict = {}

    with open(ruta_ingresos, 'r') as archivo_ingesos:
        for linea in archivo_ingesos:
            datos = linea.strip('\n').split(', ')
            cinema = datos[2]
            pelicula = datos[1]
            entradas_vendidas = int(datos[3])
            if cinema not in informacion_asientos_comprados:
                informacion_asientos_comprados[cinema] = {}
            if pelicula in informacion_asientos_comprados[cinema]:
                informacion_asientos_comprados[cinema][pelicula] += entradas_vendidas
            else:
                informacion_asientos_comprados[cinema][pelicula] = entradas_vendidas

    return informacion_asientos_comprados


def asientos_comprados_sala(dict_menu:dict, dict_del_txt:dict)->int:

    location = dict_menu['location']
    name = dict_menu['name']

    if letra_español in name:
        name = name.replace(letra_español, conversion_de_letra)
    
    if location in dict_del_txt and name in dict_del_txt[location]:
        return dict_del_txt[location][name]
    
    else:
        return 0

def obtener_asientos_disponibles(dict_menu:dict)->int:

    asientos_totales:int = obtener_cantidad_asientos(dict_menu)
    dict_del_txt:dict = saber_asientos_comprados()
    asientos_reservados:int = asientos_comprados_sala(dict_menu, dict_del_txt)

    return asientos_totales - asientos_reservados

#-----------------------------------------------------------PANTALLA_SECUNDARIA-------------------------------------------------------------------#

def ventana_informacion_pelicula(dict_menu : dict , ventana_principal)->None:

    asientos_disponibles_en_la_sala:int = obtener_asientos_disponibles(dict_menu)

    print(f'asientos disponibles: {asientos_disponibles_en_la_sala}')

    ventana_principal.withdraw()
    id_principal = dict_menu["id"]
    id, guardar = api_ventana_secundaria(id_principal)

    ventana_secundaria = Toplevel()
    ventana_secundaria.title("ventana secundaria")
    ventana_secundaria.geometry("1350x700")
    ventana_secundaria.config(background="black")
   
    botones(ventana_secundaria,ventana_principal,dict_menu,asientos_disponibles_en_la_sala)
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
    informacion_de_movies = get(url, headers=headers)

    if informacion_de_movies.status_code == 200:
        
        archivo = informacion_de_movies.json() #diccionario
        id = archivo["id"]
        nombre = archivo["name"]
        diccionario : dict = {"name": nombre, "id": id , "cinema_id": id_cine, "location": nombre_cine}
        print(diccionario)
        ventana_informacion_pelicula(diccionario,ventana)
    
#--------------------------------------------------------------------POSTERS----------------------------------------------------------------------#

def lista_posters(sub_lista : str)-> str:

    url = "http://vps-3701198-x.dattaweb.com:4000/posters/" + str(sub_lista)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == 200:
        datos = verificar_archivo.json() #diccionario
       
        for i in datos:
            variable = datos[i]

            return variable
    
#--------------------------------------------------------------------ID_DE_PELICULAS--------------------------------------------------------------#

def lista_peliculas(sub_lista : list, id : str)-> list:
    
    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas/{0}/movies".format(id)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == 200:
        datos = verificar_archivo.json() #diccionario
        
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
        verificar_archivo = get(url, headers=headers)

        if verificar_archivo.status_code == 200:

            archivo = verificar_archivo.json()
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
    imagen_a_deco_pelicula: bytes = b64decode(base64_data_pelicula)
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

def ventana_principal(numero_cine, nombre_cine, ventana_anterior):
    
    ventana_anterior.destroy()

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

def cinemas()->tuple:

    lista_id:list = []
    nombre_cine:list = []

    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    response__1 = get(url, headers=headers)

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

    cine_id,nombre_cine = cinemas()
    print(cine_id)
    print(nombre_cine)
    numero : int = 0

    for vueltas in range(len(cine_id)):
        crear_boton_cines(frame,cine_id[numero],nombre_cine[numero],ventana)
        numero += 1
    
    ventana.mainloop()
    
#----------------------------------------------------------------------APP_QR---------------------------------------------------------------------#
#--------------------------------------------------------------CREAR_QR_GUARDAR_EN_PDF------------------------------------------------------------#

def crear_qr(boleto_comprado, dict_menu, ventana_final, ventana3, ventana_principal, contador_de_snacks) -> None:

    ruta_qr: str = path.join(getcwd(), 'QR')

    if not path.exists(ruta_qr):
        makedirs(ruta_qr)

    archivos_en_qr: list[str] = listdir(ruta_qr)
    cantidad_de_archivos: int = len(archivos_en_qr)

    id_qr: str = 'QR_' + str(cantidad_de_archivos + 1)
    pelicula = dict_menu['name']
    if letra_español in pelicula:
        pelicula = pelicula.replace(letra_español, conversion_de_letra)
    cine = dict_menu['location']
    entradas: str = boleto_comprado
    tiempo: str = fecha_y_hora()
    snacks_comprados:str = ''
    for snacks in contador_de_snacks:
        if contador_de_snacks[snacks] > 0:
            snacks_comprados += f'{snacks}: {str(contador_de_snacks[snacks])}, '
    

    contenido_qr: str = f'{id_qr}, {pelicula}, {cine}, {entradas}, [{snacks_comprados}], {tiempo}'

    if ', ]' in contenido_qr:
        contenido_qr = contenido_qr.replace(', ]', ']')
    elif '[]' in contenido_qr:
        contenido_qr = contenido_qr.replace('[]', 'sin snacks')
        
    print(contenido_qr)
    ruta_imagen_qr: str = path.join(ruta_qr, f'{id_qr}.png')
    ruta_pdf: str = path.join(ruta_qr, f'{id_qr}.pdf')

    imagen = make(contenido_qr)
    imagen.save(ruta_imagen_qr)

    archivo_pdf = canvas.Canvas(ruta_pdf, pagesize=letter)

    archivo_pdf.drawInlineImage(ruta_imagen_qr, 100, 500, width=300, height=300)

    archivo_pdf.save()

    remove(ruta_imagen_qr)

    # HACER FUNCION: reestablecer_boletos_y_snacks()

    ventana_final.destroy()
    ventana_principal.deiconify()


'''def restablecer_valores_snacks(contador_de_snacks:dict)->None:
    for snack in contador_de_snacks:
        contador_de_snacks[snack] = 0'''
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

    except Exception as error:
        print(f"Error al extraer la imagen del PDF: {str(error)}")
        return False

#---------------------------------------------------------------DECODIFICANDO_QR_DESDE_IMAGEN-----------------------------------------------------#

def decodificar_qr_desde_imagen(ruta_imagen):
    #Se modifico porque al usar decode (pyzbar) tiraba error porque no reconocia la libreria
    #Lee la imagen 
    imagen = imread(ruta_imagen)
    #Pasa la imagen a escala de grises para detectar mejor
    imagen_gris = cvtColor(imagen, COLOR_BGR2GRAY)
    detector = QRCodeDetector()
    #Decodifica el qr
    datos_qr = detector.detectAndDecode(imagen_gris)

    if datos_qr:
        # Devuelve el valor del qr
        return datos_qr[0]
    else:
        return None

#-----------------------------------------------------------AGREGAR/VERIFICAR_QR_EN_TXT-----------------------------------------------------------#

def agregar_a_ingresos_txt(codigo_qr):
    # Verificar si el código QR ya está en ingresos.txt
    with open("ingresos.txt", "a") as archivo_ingresos:
        archivo_ingresos.write(f'{codigo_qr}\n')

#--------------------------------------------------------------------QR_PDF-----------------------------------------------------------------------#
def generar_ventana_emergente(mensaje : int) -> None:
    """Se creo para no repetir codigo"""
    ventana_error = Toplevel()
    ventana_error.geometry("300x200")
    ventana_error.title("ERROR !!!")

    frame_error = Frame(ventana_error, bg="black")
    frame_error.pack(expand=True, fill="both")

    mensaje = Label(frame_error, text=mensaje)
    mensaje.config(bg="black", fg="red")
    mensaje.pack(ipadx=50, ipady=50)

    boton_error = Button(frame_error, text="OK", command=ventana_error.destroy)
    boton_error.config(bg="black", fg="red")
    boton_error.pack(ipadx=25, ipady=10)

def codigo(cajon, ventana, carpeta_pdf):
    dato_entrada = cajon.get().upper()
    #print(f"Ingresaste: {dato_entrada}")

    archivo_pdf = f"{dato_entrada}.pdf"
    ruta_completa_pdf = path.join(carpeta_pdf, archivo_pdf)

    if path.exists(ruta_completa_pdf):
        #print(f"El archivo {archivo_pdf} existe.")

        # Ruta para guardar la imagen extraída
        ruta_imagen_png = path.join(carpeta_pdf, f'{dato_entrada}.png')

        # Obtener el contenido del PDF como imagen PNG
        if extraer_imagen_desde_pdf(ruta_completa_pdf, ruta_imagen_png):
            #print(f"Imagen extraída correctamente del PDF {archivo_pdf}")

            # Decodificar el código QR desde la imagen
            codigo_qr = decodificar_qr_desde_imagen(ruta_imagen_png)
            
            # Se abre en a+ para que si no existe un archivo lo cree y para que lea antes de agregar 
            with open("ingresos.txt", "a+") as archivo_lectura:
                # Por defecto la posicion al entrar es al final, con seek lee todo desde el principio
                archivo_lectura.seek(0)
                contenido_actual = archivo_lectura.read()

            if codigo_qr is not None:
                #print(f"Código QR extraído: {codigo_qr}")
                
                # Entra si no hay una linea igual
                if codigo_qr not in contenido_actual:
                    agregar_a_ingresos_txt(codigo_qr)
                    mensaje = "SE REGISTRO CORRECTAMENTE EL QR"
                    generar_ventana_emergente(mensaje)
                
                else:
                    mensaje = "CÓDIGO YA REGISTRADO"
                    generar_ventana_emergente(mensaje)
            else:
                mensaje = "No se encontró código QR en la imagen."
                generar_ventana_emergente(mensaje)
        else:
            mensaje = f"No se pudo extraer la imagen del PDF {archivo_pdf}"
            generar_ventana_emergente(mensaje)

    # Intenta encontrar la imagen para borrarla, si el pdf no existe no declara la variable
    try:
        if path.exists(ruta_imagen_png):
            # Eliminar la imagen PNG después de leer el código QR
            remove(ruta_imagen_png)

    except UnboundLocalError:
        mensaje = "NOMBRE QR NO EXISTE"
        generar_ventana_emergente(mensaje)
    # No cerrar la ventana de Tkinter

#------------------------------------------------------------------LECTURA_QR---------------------------------------------------------------------#

def qr(vent):
    #abre la camara
    camara = VideoCapture(0)
    ciclo = True
    dato_qr = ""

    while ciclo:
        #lee la imagen que capture, ret es un booleano que da True cuando se recibe un frame
        # y frame da la imagen recibida
        ret, frame = camara.read()

        #la camara se desactiva y se cierra con la letra s
        if waitKey(1) & 0xFF == ord("s"):
            ciclo = False

        #detector de qr
        detector = QRCodeDetector()
        #detectAndDecode recibe el frame y devuelve: 
        # data= contenido del qr en una cadena, si no detecta qr devuelve cadena vacia 
        # bbox= devuelve las coordenadas de los bordes del codigo qr 
        # rectifiedImage= devuelve cadena el contenido del qr con sus correcciones de errores
        data, bbox, rectifiedImage = detector.detectAndDecode(frame)

        if len(data) > 0: #si se detecta un qr
            #"web" crea la ventana
            #"rectifiedImage" muestra los datos del qr
            imshow("web", rectifiedImage)
            dato_qr = data
            #rompe el ciclo cuando recibe un qr
            ciclo = False
        else:
            #si no encuentra qr muestra el frame
            imshow("web", frame)

    #cierra la videocamara
    camara.release()
    #cierra todas las ventanas
    destroyAllWindows()

    
    with open("ingresos.txt", "a+") as archivo_lectura:
        archivo_lectura.seek(0)
        contenido_actual = archivo_lectura.read()

    if dato_qr not in contenido_actual:
        with open("ingresos.txt", "a") as archivo:
            archivo.write(dato_qr + '\n')
        mensaje = "SE REGISTRO CORRECTAMENTE EL QR"
        generar_ventana_emergente(mensaje)

    elif dato_qr in contenido_actual:
        mensaje = "CÓDIGO YA REGIDSTRAO"
        generar_ventana_emergente(mensaje)

    else:
        mensaje = "CÓDIGO INVALIDO"
        generar_ventana_emergente(mensaje)

def menu_QR():
    ventana = Tk()
    ventana.geometry("500x500")
    ventana.title("Validacion")

    frame_principal = Frame(ventana, bg="black")
    frame_principal.pack(expand=True, fill="both")

    label_1 = Label(frame_principal, text="INGRESE SU CODIGO")
    label_1.config(bg="black", fg="red")
    label_1.pack(pady=20, ipadx=50, ipady=20)

    cajon = Entry(frame_principal)
    cajon.pack(pady=20, ipadx=50)

    boton_1 = Button(frame_principal, text="VALIDAR", command=lambda: codigo(cajon, ventana, "QR"))
    boton_1.config(bg="black", fg="red")
    boton_1.pack(pady=20, ipadx=50, ipady=5)

    boton_2 = Button(frame_principal, text="ENCENDER QR", command=lambda: qr(ventana))
    boton_2.config(bg="black", fg="red")
    boton_2.pack(pady=20, ipadx=50, ipady=5)



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
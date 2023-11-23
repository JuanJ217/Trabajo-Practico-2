
from tkinter import Tk, Label, Button, Frame, Entry, Toplevel, Canvas, Scrollbar, messagebox
import tkinter as tk
from PIL import ImageTk
import base64
import requests
import cv2

PRECIO_DE_ENTRADA:int=1800.00
cantidad:str= 'cantidad'
snacks:str= 'snacks'
movies:str = 'movies'
cinemas:str = 'cinemas'
opcion_de_cinema:str = 'Caballito'

#---------------------------------------------------API_SECUNDARIA-------------------------------------------------------------------------------#

def obtener_cantidad_asientos(objetivo)->int:

    
    url = "http://vps-3701198-x.dattaweb.com:4000/" + objetivo
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    lista_de_cinemas = response.json()

    for informacion_cinemas in lista_de_cinemas:
        if informacion_cinemas['location'] == opcion_de_cinema:
            return informacion_cinemas['available_seats'] #32 asientos



def obtener_snacks(objetivo)->dict:
    url = "http://vps-3701198-x.dattaweb.com:4000/" + objetivo
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(url, headers=headers)

    return response.json() #Retorna una diccionario ya traducido de Json


def actualizar_datos_cines()->None:
    #Con esta función actualizaré la cantidad de asientos que haya para cada función de cada cine
    


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


def botones_aceptar_cancelar_snacks(ventana3, contador_de_snacks, cantidad_visible)->None:

    aceptar = Button(ventana3, text='Aceptar', command=lambda: cerrar_ventana(ventana3))
    aceptar.pack()
    aceptar.place(x=95, y=220)
    aceptar.config(fg='blue')

    cancelar = Button(ventana3, text='Cancelar compra', command=lambda: reiniciar_snacks(contador_de_snacks, ventana3, cantidad_visible))
    cancelar.pack()
    cancelar.place(x=70, y=250)
    cancelar.config(fg='red')

def botones_snacks(ventana3, informacion_snacks, contador_de_snacks)->None:

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

    botones_aceptar_cancelar_snacks(ventana3, contador_de_snacks, cantidad_visible)


def ventana_confirmar_compra(informacion_snacks, contador_de_snacks, boletos, boleto_comprado, lista_final, ventana3)->None:

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

        encabezado = Label(ventana_final, text='CARRITO', font=20)
        encabezado.pack(side='top', pady=10)
        encabezado.config(fg='white', bg='black')

        snacks_comprados(contador_de_snacks, ventana_final, informacion_snacks, lista_final)
        boletos_comprados(ventana_final, boleto_comprado)
        mostrar_precio_total(ventana_final, lista_final, boleto_comprado)

        botones_de_accion = Frame(ventana_final)
        botones_de_accion.pack(side='top', anchor='center', pady=10)
        botones_de_accion.config(bg='black')

        boton_comprar = Button(botones_de_accion, text='PAGAR', command=None)
        boton_comprar.pack(side='top', anchor='n', pady=10)

        boton_cancelar_compra = Button(botones_de_accion, text='CANCELAR', command=None)
        boton_cancelar_compra.pack(side='bottom', anchor='center')  

        ventana_final.mainloop()

def ventana_de_reservas(ventana2)->None:

    ventana2.withdraw()
    lista_final=[]
    boletos= {'disponibles': 5, 'totales': 10}
    comprar_boleto = {'cantidad': 0}
    informacion_snacks:dict = obtener_snacks(snacks)
    contador_de_snacks:dict={}
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


def ventana_de_snacks(contador_de_snacks:dict, informacion_snacks:dict)->None:

    ventana3 = Tk()
    ventana3.geometry('250x300')
    ventana3.config(bg='black')
    ventana3.resizable(width=False, height=False)

    encabezado = Label(ventana3, text='COMPRAR SNACKS')
    encabezado.pack(side='top')
    encabezado.config(fg='white', bg='black')

    botones_snacks(ventana3, informacion_snacks, contador_de_snacks)

    ventana3.mainloop()

def snacks_comprados(contador_de_snacks, ventana_final, informacion_snacks, lista_final)->None:

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

def boletos_comprados(ventana_final, boleto_comprado)->None:

    tickets = Frame(ventana_final)
    tickets.pack(side='top', anchor='w')
    tickets.config(bg='black')

    cantidad_boletos = Label(tickets, text=f'{boleto_comprado[cantidad]} Entradas', font=20)
    cantidad_boletos.pack(side='left',  anchor='w')
    cantidad_boletos.config(width=20, fg='orange', bg='black')

    precio_boletos_seleccionados = Label(tickets, text=precio_boletos(boleto_comprado), font=20)
    precio_boletos_seleccionados.pack(side='left')
    precio_boletos_seleccionados.config(fg='green', bg='black')

def mostrar_precio_total(ventana_final, lista_final, boleto_comprado)->None:

    linea_final = Frame(ventana_final)
    linea_final.pack(side='top', anchor='w', pady=15)
    linea_final.config(bg='black')

    palabra_total = Label(linea_final, text='TOTAL', font=20)
    palabra_total.pack(side='left', anchor='w')
    palabra_total.config(width=20, fg='red', bg='black')

    precio_total = Label(linea_final, text=precio_final(lista_final, boleto_comprado), font=20)
    precio_total.pack(side='left')
    precio_total.config(fg='green', bg='black')


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
        guardar.append(variable)

    return id_principal, guardar

#------------------------------------------------------------------PANTALLA---------------------------------------------------------------------#
def ventana_informacion_pelicula(dict_menu : dict , ventana1) -> Toplevel:

    ventana1.withdraw()
    id_principal = dict_menu["id"]
    id, guardar = api_ventana_secundaria(id_principal)

    ventana_secundaria = Toplevel()
    ventana_secundaria.title("ventana secundaria")
    ventana_secundaria.geometry("1350x700")
    ventana_secundaria.config(background="black")
   
    boton_menu, boton_reserva = botones(ventana_secundaria,ventana1)
    s_sala = sala(ventana_secundaria, id)
    s_sinopsis, t_sinopsis = sinopsis(ventana_secundaria, guardar)
    g_genero, t_genero = genero(ventana_secundaria, guardar)
    a_actores, t_actores = actores(ventana_secundaria, guardar)
    d_duracion, t_duracion = duracion(ventana_secundaria,guardar)
    ventana_secundaria.mainloop()

    return ventana_secundaria

#---------------------------------------------------VOLVER AL MENU / RESEVAR--------------------------------------------------------------------#
def volver_al_menu(ventana_secundaria,ventana1):

    ventana1.iconify()
    ventana1.deiconify()
    ventana_secundaria.destroy()


def ir_a_reservar(ventana_secundaria):
    
    ventana3 = Toplevel()
    ventana3.title("reservar")
    ventana3.geometry("1000x600")
    ventana3.config(background="black")

#------------------------------------------------------------------BOTONES-----------------------------------------------------------------------#

def botones (ventana_secundaria,ventana1) -> tuple:

    '''
    BTN-VOLVER AL MENU
        PRE CONDICION: el usuario clickea el boton
        POST CONDICION: al clickear el boton se cerrara la ventana secundaria y se volvera a al menu

    BTN-RESERVAR
        PRE CONDICION: el usuario clickea el boton
        POST CONDICION: al clickear el boton se abrira la ventana 3
    '''

    boton_volver_al_menu = Button(ventana_secundaria,  text= "VOLVER AL MENU", 
                                  background= "black",  fg="gold", 
                                  width= 20,           height= 5, 
                                  command= lambda: volver_al_menu(ventana_secundaria,ventana1))
       
    boton_volver_al_menu.place(relx=0.1, rely=0.1, anchor=tk.CENTER)

    boton_reservar = Button(ventana_secundaria,  text= "RESERVAR", 
                            background= "black",  fg="gold",  
                            width= 20,          height= 5,
                            command= lambda: ventana_de_reservas(ventana_secundaria))
    
    boton_reservar.place(relx=0.88, rely=0.9, anchor=tk.CENTER)

    return boton_volver_al_menu, boton_reservar

#------------------------------------------------------------------------SALA-------------------------------------------------------------------#

def sala(ventana_secundaria, id) -> Label:

    sala_proyectar = Label(
                            ventana_secundaria,   text= "SALA  " + id,
                            background= "black",  fg="red",    
                            )
    sala_proyectar.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

    return sala_proyectar

#------------------------------------------------------------------SINOPSIS---------------------------------------------------------------------#

def sinopsis(ventana_secundaria, guardar) -> tuple: 

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

    return sinopsis, texto_sinopsis
#---------------------------------------------------------------------GENERO-------------------------------------------------------------------#

def genero(ventana_secundaria, guardar) -> tuple:

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
    
    return genero, texto_genero
#----------------------------------------------------------------------ACTORES-------------------------------------------------------------------#

def actores(ventana_secundaria, guardar) -> tuple:

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

    return actores, texto_actores

#---------------------------------------------------------------------DURACION-------------------------------------------------------------------#
def duracion(ventana_secundaria, guardar) -> tuple:

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

    return duracion, texto_duracion

#--------------------------------------------------------HAY ASIENTOS?--------------------------------------------------------------------------#
def no_hay_lugar():

        mensaje = messagebox.showinfo("Lo sentimos, no hay mas asientos disponibles para ver esta pelicula por favor vuelva al menu")
#---------------------------------------------------------PARTE CRIS---------------------------------------------------------------------------#


#------------------------------------------------BOTON DE ACCESO A VENTANA 2 ---------------------------------------------------------------------#

def boton_peliculas(sub_id : int,ventana):

    url = "http://vps-3701198-x.dattaweb.com:4000/movies/" + str(sub_id)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"


    headers = {'Authorization': f'Bearer {token}'} #llave de acceso

    response__1 = requests.get(url, headers=headers)


    if response__1.status_code == 200:
        
        archivo = response__1.json() #diccionario
        id = archivo["id"]
        nombre = archivo["name"]
        diccionario : dict = {"name": nombre,"id": id , "cinema_id": 1,"location": "Caballito"}
        print(diccionario)
        ventana_informacion_pelicula(diccionario,ventana)
    
#------------------------------------------------POSTERS----------------------------------------------------------------------------#

def lista_posters(sub_lista : str)->str:

    url = "http://vps-3701198-x.dattaweb.com:4000/posters/" + str(sub_lista)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    response__1 = requests.get(url, headers=headers)

    if response__1.status_code == 200:
        datos = response__1.json() #diccionario
       
        for i in datos:
            variable = datos[i]

            return variable
    
    
#-------------------------------------------- ID DE PELICULAS --------------------------------------------------------------------#

def lista_peliculas(sub_lista : list)->list:
    
    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas/1/movies"
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


#-----------------------------------------------BUSCAR PELICULAS --------------------------------------------------------------------#

def buscar(cajon, ventana, sub_lista_de_peliculas):

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
                diccionario : dict = {"name" : datos ,"id" : id , "cinema_id": 1,"location": "Caballito"}

                print(diccionario)
                ventana_informacion_pelicula(diccionario,ventana)

       
    else:
        sub_ventana = Toplevel()
        sub_ventana.geometry("300x200")
        sub_ventana.title("ERROR !!!")

        sub_frame = Frame(sub_ventana,bg="black")
        sub_frame.pack(expand=True,fill="both")

        
        mensaje = Label(sub_frame,text="NO SE ENCONTRO LA PELICULA. INTENTE DE NUEVO")
        mensaje.config(bg="black",fg="red")
        mensaje.pack(ipadx=50,ipady=50)

        sub_boton = Button(sub_frame,text = "OK",command=sub_ventana.destroy)
        sub_boton.config(bg="black",fg="red")
        sub_boton.pack(ipadx=25,ipady=10)

#-------------------------------------------------------VENTANA PRINCIPAL -----------------------------------------------------------------#

def ventana1():

    print(obtener_cantidad_asientos(cinemas))

    ventana = Tk()
    ventana.geometry("1600x720")
    ventana.title("TOTEM CINEMA")

    fram_1 = Frame(ventana, bg="black")
    fram_1.config(relief="raised", bd=25)
    fram_1.pack(fill="x")

    cajon = Entry(fram_1)
    cajon.grid(row=0, column=0, ipadx=100, ipady=5)

    listas_de_peliculas = lista_peliculas([])

    boton_busqueda = Button(fram_1, text="BUSCAR", command=lambda: buscar(cajon, ventana, listas_de_peliculas))
    boton_busqueda.config(bg="black", fg="red")
    boton_busqueda.grid(row=0, column=1, padx=270, ipadx=30, ipady=5)

    ubicacion = Label(fram_1, text="CINE : CABALLITO")
    ubicacion.config(bg="black", fg="red")
    ubicacion.grid(row=0, column=2, padx=100, ipadx=30, ipady=5)

    imagen_ejecutable = ejecucion_boton_pelicula(listas_de_peliculas, ventana)

    ventana.mainloop()


def configurar_frame_canvas_scrollbar(ventana:None, side:str)->tuple:

    frame = Frame(ventana, bg="black", height=1000, width=600)
    frame.config(relief="raised", bd=25)
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


def crear_boton_pelicula(sub_frame, imagen, pelicula_info, ventana, row, column):
    boton_pelicula = Button(sub_frame, image=imagen, bg="black",
                            command=lambda info=pelicula_info: boton_peliculas(info, ventana))
    
    boton_pelicula.grid(row=row, column=column)

def cargar_imagen_pelicula(pelicula_info):

    funcion_pelicula = lista_posters(pelicula_info)
    base64_data_pelicula = funcion_pelicula.split(",")[1]
    imagen_a_deco_pelicula = base64.b64decode(base64_data_pelicula)
    imagen_capturada_pelicula = ImageTk.PhotoImage(data=imagen_a_deco_pelicula)

    return imagen_capturada_pelicula

def ejecucion_boton_pelicula(listas_de_peliculas, ventana):

    sub_frame_1 = configurar_frame_canvas_scrollbar(ventana, "left")
    sub_frame_2 = configurar_frame_canvas_scrollbar(ventana, "right")

    lista_imagenes = []

    for i in range(13):
        pelicula_info = listas_de_peliculas[i]
        imagen_pelicula = cargar_imagen_pelicula(pelicula_info)
        lista_imagenes.append(imagen_pelicula)
        if i < 6:
            sub_frame = sub_frame_1
        else:
            sub_frame = sub_frame_2
        crear_boton_pelicula(sub_frame, imagen_pelicula, pelicula_info, ventana, row=i // 3, column=i % 3)

    return lista_imagenes



def qr(vent):

    camara = cv2.VideoCapture(0)
# 
    ciclo : bool = True
    dato_qr : str = ""

    while ciclo:

        ret,frame = camara.read()

        if cv2.waitKey(1) & 0xFF == ord("s"):
            ciclo : bool = False

        detector = cv2.QRCodeDetector()
        data,bbox,rectifiedImage = detector.detectAndDecode(frame)

        if len(data) > 0:
            
            cv2.imshow("web",rectifiedImage)

            dato_qr = data

            ciclo : bool = False
        else:
            cv2.imshow("web",frame)

    camara.release()
    cv2.destroyAllWindows()

    print(dato_qr)
    archivo = open("memoria.txt","r+")
    sub_archivo = archivo.readlines()
    archivo.close()

    empaquetar_datos : list = list(map(mapeo,sub_archivo))

    if dato_qr in empaquetar_datos:

        subir_archivo = open("base_de_datos.txt","w")

        subir_archivo.write(dato_qr)
        subir_archivo.close()
        vent.destroy()

    else:
        vetana_error = Toplevel()
        vetana_error.geometry("300x200")
        vetana_error.title("ERROR !!!")

        frame_error = Frame(vetana_error,bg="black")
        frame_error.pack(expand=True,fill="both")

        
        mensaje = Label(frame_error,text="CODIGO INVALIDO")
        mensaje.config(bg="black",fg="red")
        mensaje.pack(ipadx=50,ipady=50)

        boton_error = Button(frame_error,text = "OK",command=vetana_error.destroy)
        boton_error.config(bg="black",fg="red")
        boton_error.pack(ipadx=25,ipady=10)





def mapeo(lista_base: list):

    corte = lista_base.strip("\n")
    separar = corte.split(",")
    
    return separar

def codigo(cajon,vent):
    dato_entrada = cajon.get().lower()

    print(dato_entrada)
    archivo = open("memoria.txt","r+")
    sub_archivo = archivo.readlines()
    archivo.close()
    
    empaquetar_datos : list = list(map(mapeo,sub_archivo))
    print(empaquetar_datos)
    lista_de_codigos : list = []

    for vuelta in empaquetar_datos:
        lista_de_codigos.append(vuelta[0])
    print(lista_de_codigos)

    if dato_entrada in lista_de_codigos:
        subir_archivo = open("base_de_datos.txt","w")

        dato_a_subir : str = ""
        
        for sub_vueltas in empaquetar_datos:

            if dato_entrada == sub_vueltas[0]:

                concatenar = ",".join(sub_vueltas)
                dato_a_subir = concatenar
        
        subir_archivo.write(dato_a_subir)
        subir_archivo.close()
        vent.destroy()

    else:
        vetana_error = Toplevel()
        vetana_error.geometry("300x200")
        vetana_error.title("ERROR !!!")

        frame_error = Frame(vetana_error,bg="black")
        frame_error.pack(expand=True,fill="both")

        
        mensaje = Label(frame_error,text="CODIGO INVALIDO")
        mensaje.config(bg="black",fg="red")
        mensaje.pack(ipadx=50,ipady=50)

        boton_error = Button(frame_error,text = "OK",command=vetana_error.destroy)
        boton_error.config(bg="black",fg="red")
        boton_error.pack(ipadx=25,ipady=10)

def menu_QR()->None:
    ventana= tk.Tk()
    ventana.geometry("500x500")
    ventana.title("Validacion")

    frame_principal = Frame(ventana,bg="black")
    frame_principal.pack(expand=True,fill="both")

    label_1 = Label(frame_principal,text="INGRESE SU CODIGO")
    label_1.config(bg="black",fg="red")
    label_1.pack(pady=20,ipadx=50,ipady=20)

    cajon = Entry(frame_principal)
    cajon.pack(pady=20,ipadx=50)

    boton_1 = Button(frame_principal,text="VALIDAR",command= lambda : codigo(cajon,ventana))
    boton_1.config(bg="black",fg="red")
    boton_1.pack(pady=20,ipadx=50,ipady=5)

    boton_2 = Button(frame_principal,text="ENCENDER QR",command= lambda : qr(ventana))
    boton_2.config(bg="black",fg="red")
    boton_2.pack(pady=20,ipadx=50,ipady=5)

    ventana.mainloop()


def menu()->str:
    print('MENU DEL CINE')
    print()
    print('1) APP CINE')
    print('2) App QR')
    print('3) Salir del menú')
    print()
    return str(input('Elija opción: '))

def main():
    sigamos:bool = True
    while sigamos:
        respuesta = menu()
        if respuesta == '1':
            ventana1()
        elif respuesta == '2':
            menu_QR()
        elif respuesta == '3':
            sigamos:bool = False
main()
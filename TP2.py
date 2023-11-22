
from tkinter import Tk, Label, Button , Frame , Entry, Toplevel ,PhotoImage, Canvas,Scrollbar,messagebox
import tkinter as tk
from PIL import ImageTk, Image
import base64
import requests

PRECIO_DE_ENTRADA:int=1800.00
cantidad:str= 'cantidad'
snacks:str= 'snacks'
movies:str = 'movies'

#---------------------------------------------------API_SECUNDARIA-------------------------------------------------------------------------------#

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


def ventana_de_reservas(ventana2)->None:

    ventana2.withdraw()
    lista_final=[]
    boletos= {'disponibles': 5, 'totales': 10}
    comprar_boleto = {'cantidad': 0}
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

    botones_snacks(ventana3, informacion_snacks, contador_de_snacks)

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
def ventana2(dict_menu : dict , ventana1) -> Toplevel:

    ventana1.withdraw()
    id_principal = dict_menu["id"]
    id, guardar = api_ventana_secundaria(id_principal)

    ventana_secundaria = Toplevel()
    ventana_secundaria.title("ventana secundaria")
    ventana_secundaria.geometry("1350x700")
    ventana_secundaria.config(background="black")

    #llamada a las funciones de la pantalla secundaria/pantalla 2 
   
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
    boton_volver_al_menu = Button(
                                    ventana_secundaria,  text= "VOLVER AL MENU", 
                                    background= "black",  fg="gold", 
                                    width= 20,           height= 5, 
                                    command= lambda: volver_al_menu(ventana_secundaria,ventana1)
                                    )   
    boton_volver_al_menu.place(relx=0.1, rely=0.1, anchor=tk.CENTER)

    boton_reservar = Button(
                            ventana_secundaria,  text= "RESERVAR", 
                            background= "black",  fg="gold",  
                            width= 20,          height= 5,
                            command= lambda: ventana_de_reservas(ventana_secundaria)  
                            )
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
        ventana2(diccionario,ventana)
    
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

def buscar(cajon, ventana,sub_lista_de_peliculas):
    datos = cajon.get().upper()
    
    lista_de_peliculas : list = []
    lista_completa : list = []
    
    for vueltas in sub_lista_de_peliculas:
        url = "http://vps-3701198-x.dattaweb.com:4000/movies/{0}".format(vueltas)
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"


        headers = {'Authorization': f'Bearer {token}'} #llave de acceso

        response__1 = requests.get(url, headers=headers)


        if response__1.status_code == 200:
            archivo = response__1.json() #diccionario
            lista_de_peliculas.append(archivo["name"])
            lista_completa.append(archivo)
            

    

    if datos in lista_de_peliculas:

        for sub_vueltas in lista_completa:

            if datos == sub_vueltas["name"]:

                id = sub_vueltas["id"]
                diccionario : dict = {"name" : datos ,"id" : id , "cinema_id": 1,"location": "Caballito"}

                print(diccionario)
                ventana2(diccionario,ventana)

       
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
    ventana = Tk()
    ventana.geometry("1600x720")
    ventana.title("TOTEM CINEMA")

    fram_1 = Frame(ventana,bg="black")
    fram_1.config(relief="raised",bd=25)
    fram_1.pack(fill="x")


    fram_2 = Frame(ventana,bg="black",height=1000, width=600)
    fram_2.config(relief="raised",bd=25)
    fram_2.pack(side=tk.RIGHT ,fill=tk.BOTH,expand=True)

    fram_3 = Frame(ventana,bg="black",height=1000, width=600)
    fram_3.config(relief="raised",bd=25)
    fram_3.pack(side=tk.LEFT ,fill=tk.BOTH, expand=True)


    cajon = Entry(fram_1)
    cajon.grid(row=0,column=0,ipadx=100,ipady=5)


    listas_de_peliculas : list = lista_peliculas([])

    boton_busqueda = Button(fram_1,text="BUSCAR",command=lambda : buscar(cajon,ventana,listas_de_peliculas))
    boton_busqueda.config(bg="black",fg="red")
    boton_busqueda.grid(row=0,column=1,padx=270,ipadx=30,ipady=5)

    ubicacion = Label(fram_1, text = "CINE : CABALLITO")
    ubicacion.config(bg="black",fg="red")
    ubicacion.grid(row=0,column=2,padx = 100 ,ipadx=30,ipady=5)


    canvas_1 = Canvas(fram_2,bg="black")
    canvas_1.pack(side="left", fill="both", expand=True)

    scroll_1 = Scrollbar(fram_2,orient="vertical",command=canvas_1.yview)
    scroll_1.pack(side="right",fill="y")

    canvas_1.config(yscrollcommand=scroll_1.set)
    canvas_1.bind("<Configure>", lambda e: canvas_1.configure(scrollregion=canvas_1.bbox("all")))

    sub_frame_1 = Frame(canvas_1,bg="black")

    canvas_1.create_window((0,0),window=sub_frame_1,anchor="nw")




    canvas_2 = Canvas(fram_3,bg="black")
    canvas_2.pack(side="left", fill="both", expand=True)

    scroll_2 = Scrollbar(fram_3,orient="vertical",command=canvas_2.yview)
    scroll_2.pack(side="right",fill="y")

    canvas_2.config(yscrollcommand=scroll_2.set)
    canvas_2.bind("<Configure>", lambda e: canvas_2.configure(scrollregion=canvas_2.bbox("all")))

    sub_frame_2 = Frame(canvas_2,bg="black")

    canvas_2.create_window((0,0),window=sub_frame_2,anchor="nw")

    funcion_1 = lista_posters(listas_de_peliculas[0])
    base64_data = funcion_1.split(",")[1]
    imagen_a_deco = base64.b64decode(base64_data)       
    imagen_capturada = ImageTk.PhotoImage(data=imagen_a_deco)
    boton_1 = Button(sub_frame_2,image=imagen_capturada,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[0],ventana))
    boton_1.grid(row=0,column=0)


    funcion_2 = lista_posters(listas_de_peliculas[1])
    base64_data_2 = funcion_2.split(",")[1]
    imagen_a_deco_2 = base64.b64decode(base64_data_2)           
    imagen_capturada_2 = ImageTk.PhotoImage(data=imagen_a_deco_2)
    boton_2 = Button(sub_frame_2,image=imagen_capturada_2,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[1],ventana))
    boton_2.grid(row=0,column=1)

    funcion_3 = lista_posters(listas_de_peliculas[2])
    base64_data_3 = funcion_3.split(",")[1]
    imagen_a_deco_3 = base64.b64decode(base64_data_3)           
    imagen_capturada_3 = ImageTk.PhotoImage(data=imagen_a_deco_3)
    boton_3 = Button(sub_frame_2,image=imagen_capturada_3,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[2],ventana))
    boton_3.grid(row=0,column=2)

    funcion_4 = lista_posters(listas_de_peliculas[3])
    base64_data_4 = funcion_4.split(",")[1]
    imagen_a_deco_4 = base64.b64decode(base64_data_4)           
    imagen_capturada_4 = ImageTk.PhotoImage(data=imagen_a_deco_4)
    boton_4 = Button(sub_frame_2,image=imagen_capturada_4,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[3],ventana))
    boton_4.grid(row=1,column=0)

    funcion_5 = lista_posters(listas_de_peliculas[4])
    base64_data_5 = funcion_5.split(",")[1]
    imagen_a_deco_5 = base64.b64decode(base64_data_5)           
    imagen_capturada_5 = ImageTk.PhotoImage(data=imagen_a_deco_5)
    boton_5 = Button(sub_frame_2,image=imagen_capturada_5,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[4],ventana))
    boton_5.grid(row=1,column=1)

    funcion_6 = lista_posters(listas_de_peliculas[5])
    base64_data_6 = funcion_6.split(",")[1]
    imagen_a_deco_6 = base64.b64decode(base64_data_6)           
    imagen_capturada_6 = ImageTk.PhotoImage(data=imagen_a_deco_6)
    boton_6 = Button(sub_frame_2,image=imagen_capturada_6,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[5],ventana))
    boton_6.grid(row=1,column=2)

    funcion_7 = lista_posters(listas_de_peliculas[6])
    base64_data_7 = funcion_7.split(",")[1]
    imagen_a_deco_7 = base64.b64decode(base64_data_7)           
    imagen_capturada_7 = ImageTk.PhotoImage(data=imagen_a_deco_7)
    boton_7 = Button(sub_frame_2,image=imagen_capturada_7,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[6],ventana))
    boton_7.grid(row=2,column=0)

    funcion_8 = lista_posters(listas_de_peliculas[7])
    base64_data_8 = funcion_8.split(",")[1]
    imagen_a_deco_8 = base64.b64decode(base64_data_8)           
    imagen_capturada_8 = ImageTk.PhotoImage(data=imagen_a_deco_8)
    boton_8 = Button(sub_frame_1,image=imagen_capturada_8,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[7],ventana))
    boton_8.grid(row=0,column=0)

    funcion_9 = lista_posters(listas_de_peliculas[8])
    base64_data_9 = funcion_9.split(",")[1]
    imagen_a_deco_9 = base64.b64decode(base64_data_9)           
    imagen_capturada_9 = ImageTk.PhotoImage(data=imagen_a_deco_9)
    boton_9 = Button(sub_frame_1,image=imagen_capturada_9,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[8],ventana))
    boton_9.grid(row=0,column=1)

    funcion_10 = lista_posters(listas_de_peliculas[9])
    base64_data_10 = funcion_10.split(",")[1]
    imagen_a_deco_10 = base64.b64decode(base64_data_10)           
    imagen_capturada_10 = ImageTk.PhotoImage(data=imagen_a_deco_10)
    boton_10 = Button(sub_frame_1,image=imagen_capturada_10,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[9],ventana))
    boton_10.grid(row=0,column=2)

    funcion_11 = lista_posters(listas_de_peliculas[10])
    base64_data_11 = funcion_11.split(",")[1]
    imagen_a_deco_11 = base64.b64decode(base64_data_11)           
    imagen_capturada_11 = ImageTk.PhotoImage(data=imagen_a_deco_11)
    boton_11 = Button(sub_frame_1,image=imagen_capturada_11,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[10],ventana))
    boton_11.grid(row=1,column=0)

    funcion_12 = lista_posters(listas_de_peliculas[11])
    base64_data_12 = funcion_12.split(",")[1]
    imagen_a_deco_12 = base64.b64decode(base64_data_12)           
    imagen_capturada_12 = ImageTk.PhotoImage(data=imagen_a_deco_12)
    boton_12 = Button(sub_frame_1,image=imagen_capturada_12,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[11],ventana))
    boton_12.grid(row=1,column=1)

    funcion_13 = lista_posters(listas_de_peliculas[12])
    base64_data_13 = funcion_13.split(",")[1]
    imagen_a_deco_13 = base64.b64decode(base64_data_13)           
    imagen_capturada_13 = ImageTk.PhotoImage(data=imagen_a_deco_13)
    boton_13 = Button(sub_frame_1,image=imagen_capturada_13,bg="black",command= lambda:boton_peliculas(listas_de_peliculas[12],ventana))
    boton_13.grid(row=1,column=2)




    ventana.mainloop()

def main():
    ventana1()


main()
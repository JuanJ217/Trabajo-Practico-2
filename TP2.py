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

ACEPTADO:int = 200
PRECIO_DE_ENTRADA:int = 1800.00
NO_HAY_SNACK_COMPRADO:int = 0
NO_HAY_ASIENTOS_DISPONIBLES:int = 0
INICIAL:int = 4
FINAL:int = 8
AUMENTAR_EN_UNO:int = 1
NOMBRE_CINEMA:int = 2
NOMBRE_PELICULA:int = 1
CANT_ENTRADAS_VENDIDAS:int = 3
INFO_SINOPSIS:int = 0
INFO_GENERO_PELICULA:int= 1
INFO_DURACION_PELICULA:int = 2
INFO_ACTORES:int = 3


#------------------------------------------------FUNCIONES_PARA_LA_VENTANA_DEL_CARRITO_PAGAR-----------------------------------------------------------------------------

def fecha_y_hora() -> str:

    estructura = localtime()

    return strftime('%Y-%m-%d %H:%M:%S', estructura)


def ajustar_cadena(contenido_qr:str) -> str:

    if ', ]' in contenido_qr:
        contenido_qr = contenido_qr.replace(', ]', ']')

    elif '[]' in contenido_qr:
        contenido_qr = contenido_qr.replace('[]', 'sin snacks')
    
    return contenido_qr


def crear_cadena_informacion_QR(cantidad_de_archivos:int, dict_menu:dict, boleto_comprado:str, 
                                contador_de_snacks:dict, ruta_qr:list[str])->str:
    
    '''
    PRE-CONDICION: CREARÁ LA CADENA (INFORMACION) Y LE NOMBRE DEL PDF TENIENDO EN CUENTA LA 
                   CANTIDAD DE ARCHIVOS QUE HAYA DENTRO DE LA CARPETA 'QR'. VALIDANDO QUE SI SE ELIMINAR
                   ALGÚN PDF, NO SE OBTENDRÁ UN CÓÐIGO REPETIDO
    POST-CONDICION: ALMACENARÁ LOS ARCHIVOS PDF DENTRO DE LA CARPETA 'QR', LA CUAL USAREMOS PARA
                    EXTRAER LA INFORMACION DEL QR Y PASARLA AL ARCHIVO 'INGRESOS.TXT'
    ''' 

    letra_español:str = 'Ñ'
    conversion_de_letra:str = 'NI'

    valor_numerico_codigo:int = (cantidad_de_archivos + AUMENTAR_EN_UNO)
    id_qr:str = 'QR_' + str(valor_numerico_codigo)
    codigo_qr:str = id_qr + '.pdf'
    for codigos_pdf in listdir(ruta_qr):
        if codigo_qr == codigos_pdf:
            valor_numerico_codigo += AUMENTAR_EN_UNO
            id_qr:str = 'QR_' + str(valor_numerico_codigo)
            codigo_qr:str = id_qr + '.pdf'


    pelicula:str = dict_menu['name']
    if letra_español in pelicula:
        pelicula = pelicula.replace(letra_español, conversion_de_letra)
    cine = dict_menu['location']
    entradas:str = boleto_comprado
    tiempo:str = fecha_y_hora()
    snacks_comprados:str = ''
    for snacks in contador_de_snacks:
        if contador_de_snacks[snacks] > NO_HAY_SNACK_COMPRADO:
            snacks_comprados += f'{snacks}: {str(contador_de_snacks[snacks])}, '

    contenido_qr:str = f'{id_qr}, {pelicula}, {cine}, {entradas}, [{snacks_comprados}], {tiempo}'

    contenido_qr_final:str = ajustar_cadena(contenido_qr)
        
    return id_qr, contenido_qr_final


def crear_qr_pdf(boleto_comprado:str, dict_menu:dict, ventana_final, ventana_principal, contador_de_snacks:dict) -> None:

    '''
    PRE_CONDICION: CUANDO TENGAMOS LA CARPETA 'QR', NO INGRESAR NINGúN OTRO ARCHIVO QUE
                   NO SEA EL QUE SE CREE ACÁ
    POST_CONDICON: PARA ESO SIRVE LA CARPETA, SOLO ALMACENAR ESTE TIPO DE ARCHIVO
    '''

    ruta_qr:list[str] = path.join(getcwd(), 'QR')

    if not path.exists(ruta_qr):
        makedirs(ruta_qr)

    archivos_en_qr: list[str] = listdir(ruta_qr)
    cantidad_de_archivos: int = len(archivos_en_qr)    

    id_qr, contenido_qr = crear_cadena_informacion_QR(cantidad_de_archivos, dict_menu, boleto_comprado, contador_de_snacks, ruta_qr)
    print(contenido_qr)

    ruta_imagen_qr: str = path.join(ruta_qr, f'{id_qr}.png')
    ruta_pdf: str = path.join(ruta_qr, f'{id_qr}.pdf')

    imagen = make(contenido_qr)
    imagen.save(ruta_imagen_qr)

    archivo_pdf = canvas.Canvas(ruta_pdf, pagesize=letter)
    archivo_pdf.drawInlineImage(ruta_imagen_qr, 100, 500, width=300, height=300)
    archivo_pdf.save()

    remove(ruta_imagen_qr)

    ventana_final.destroy()
    ventana_principal.deiconify()


def precio_por_snack(nombre_snack, cantidad_snack:dict, precio_snack:dict, lista_final:list[int]) -> str:

    precio_final = cantidad_snack[nombre_snack] * float(precio_snack[nombre_snack])
    lista_final.append(precio_final)

    return str(precio_final)


def precio_boletos(cantidad_entradas:str) -> str:

    return str(int(cantidad_entradas)*PRECIO_DE_ENTRADA)


def snacks_comprados(contador_de_snacks:dict, ventana_final, informacion_snacks:dict, lista_final:list[int])-> None:

    for nombre_snacks in contador_de_snacks:

        cantidades = Frame(ventana_final, bg='black')
        cantidades.pack(side='top', anchor='w')
        
        if contador_de_snacks[nombre_snacks] > NO_HAY_SNACK_COMPRADO:
            
            snacks_seleccionados = Label(cantidades, font=20, width=25, fg='orange', bg='black', 
                                         text=f'{contador_de_snacks[nombre_snacks]} {nombre_snacks}')
            snacks_seleccionados.pack(side='left')
          
            precio_snacks_seleccionados = Label(cantidades, font=20, fg='green', bg='black', 
                                                text= precio_por_snack(nombre_snacks, contador_de_snacks,
                                                                                       informacion_snacks, lista_final))
            precio_snacks_seleccionados.pack(side='left')


def boletos_comprados(ventana_final, cant_boletos_comprados:str) -> None:

    tickets = Frame(ventana_final,bg='black')
    tickets.pack(side='top', anchor='w')
  
    cantidad_boletos = Label(tickets, text=f'{cant_boletos_comprados} Entradas', 
                             font=20, width=25, 
                             fg='orange', bg='black')
    cantidad_boletos.pack(side='left',  anchor='w')

    precio_boletos_seleccionados = Label(tickets, text=precio_boletos(cant_boletos_comprados),
                                         font=20, fg='green', 
                                         bg='black')
    precio_boletos_seleccionados.pack(side='left')


def precio_final(lista_final:list[int], cantidad_entradas:str) -> str:

    boletos: float = float(precio_boletos(cantidad_entradas))
    total: int = 0

    for precios in lista_final:
        total+=precios

    return str(total+boletos)


def mostrar_precio_total(ventana_final, lista_final:list[int], boleto_comprado:str) -> None:

    linea_final = Frame(ventana_final, bg='black')
    linea_final.pack(side='top', anchor='w', pady=15)

    palabra_total = Label(linea_final, text='TOTAL',
                          font=20,     width=25, 
                          fg='red',    bg='black')
    palabra_total.pack(side='left', anchor='w')

    precio_total = Label(linea_final, text=precio_final(lista_final, boleto_comprado),
                         fg='green',  bg='black', font=20)
    precio_total.pack(side='left')

def mostrar_encabezados(ventana_final, dict_menu:dict) -> None:

    name = 'name'
    encabezado = Label(
                            ventana_final, text=f'CARRITO PARA:', 
                            font=20, fg='white', bg='black'
                        )
    encabezado.pack(side='top', pady=5)

    nombre_pelicula = Label(ventana_final, text=f'{dict_menu[name]}', font=20, fg='white', bg='black')
    nombre_pelicula.pack(pady=10)


def botones_pantalla_final(ventana_final, ventana_principal, cantidad_entradas:str, dict_menu:dict, 
                            ventana3, contador_de_snacks:dict) -> None:

    botones_de_accion = Frame(ventana_final, bg='black')
    botones_de_accion.pack(side='top', anchor='center', pady=10)
    
    boton_pagar = Button(botones_de_accion, text='PAGAR', fg='blue', 
                         command=lambda: crear_qr_pdf(cantidad_entradas, dict_menu, ventana_final, 
                                                  ventana_principal, contador_de_snacks))
    boton_pagar.pack(side='top', anchor='n', pady=10)

    boton_cancelar_compra = Button(botones_de_accion, text='CANCELAR', fg='red', 
                                   command=lambda: cancelar_compra(ventana3, ventana_final))
    boton_cancelar_compra.pack(side='bottom', anchor='center', pady=10) 


def advertencia_no_boletos_comprados(ventana_anterior) -> None:

    ventana_anterior.withdraw()
    messagebox.showwarning('Advertencia', 'No hay boletos seleccionados')
    ventana_anterior.deiconify()
    

def advertencia_asientos_excedidos(ventana_anterior, asientos_disponibles_en_la_sala:int) -> None:

    ventana_anterior.withdraw()
    messagebox.showwarning('Advertencia', f'No puedes comprar más de {asientos_disponibles_en_la_sala} asientos')
    ventana_anterior.deiconify()


def ejecucion_ventana_confirmar_compra(ventana_anterior, dict_menu:dict, contador_de_snacks:dict, informacion_snacks:dict, 
                                       lista_final:list[int], cantidad_entradas:str, ventana_principal) -> None:

    ventana_anterior.withdraw()

    ventana_final = Toplevel()
    ventana_final.geometry('352x400')
    ventana_final.config(bg='black')
    ventana_final.resizable(width=False, height=False)

    mostrar_encabezados(ventana_final, dict_menu)        
    snacks_comprados(contador_de_snacks, ventana_final, informacion_snacks, lista_final)
    boletos_comprados(ventana_final, cantidad_entradas)
    mostrar_precio_total(ventana_final, lista_final, cantidad_entradas)
    botones_pantalla_final(ventana_final, ventana_principal, cantidad_entradas, dict_menu, ventana_anterior, contador_de_snacks) 

    ventana_final.mainloop()



def confirmar_compra(informacion_snacks:dict, contador_de_snacks:dict, asientos_disponibles_en_la_sala:int,
                     lista_final:list[int], ventana3, dict_menu:dict, eleccion_entradas:str, ventana_principal) -> None:
    
    cantidad_entradas = eleccion_entradas.get()

    if cantidad_entradas == '0' or cantidad_entradas == '':
        advertencia_no_boletos_comprados(ventana3)
    
    elif int(cantidad_entradas) > asientos_disponibles_en_la_sala:
        advertencia_asientos_excedidos(ventana3, asientos_disponibles_en_la_sala)

    else:
        ejecucion_ventana_confirmar_compra(ventana3, dict_menu, contador_de_snacks, informacion_snacks, 
                                       lista_final, cantidad_entradas, ventana_principal)


#-----------------------------------------------FUNCIONES_PARA_LA_VENTANA_QUE_SE_COMPRA_ENTRADAS_Y_SNACKS--------------------------------------------------------------


def obtener_snacks() -> dict:

    url = "http://vps-3701198-x.dattaweb.com:4000/snacks"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == ACEPTADO:
        diccionario_snacks = verificar_archivo.json()

    return diccionario_snacks #Retorna una diccionario ya traducido de Json

def cantidad_de_snacks(informacion_snacks:dict, contador_de_snacks:dict) -> None:

    for snack in informacion_snacks:
        contador_de_snacks[snack]=0


def reiniciar_snacks(contador_de_snacks:dict, ventana, cantidad_visible:dict, ventana_reserva) -> None:

    for snack in contador_de_snacks:
        contador_de_snacks[snack]=0
        cantidad_visible.config(text=f'{snack}: 0')

    ventana.destroy()
    ventana_reserva.deiconify()


def cancelar_compra(ventana_anterior, ventana_actual) -> None:

    ventana_actual.destroy()
    ventana_anterior.deiconify()


def aumentar_snacks(snack:str, contador_de_snacks:dict, cantidad_visible:str) -> None:

    contador_de_snacks[snack]+=1
    cantidad_visible.config(text=f'{snack}: {contador_de_snacks[snack]}')


def disminuir_snacks(snack:str, contador_de_snacks:dict, cantidad_visible:str) -> None:

    if contador_de_snacks[snack]>0:
        contador_de_snacks[snack]-=1
        cantidad_visible.config(text=f'{snack}: {contador_de_snacks[snack]}')


def cerrar_ventana(ventana, ventana_reserva)-> None:

    ventana.destroy()
    ventana_reserva.deiconify()


def botones_aceptar_cancelar_snacks(ventana3, contador_de_snacks:dict, cantidad_visible:str, ventana_reserva) -> None:

    aceptar = Button(ventana3, text='Aceptar', 
                     command=lambda: cerrar_ventana(ventana3, ventana_reserva),
                     fg='blue', font=15)
    aceptar.pack()
    aceptar.place(x=120, y=220)
   
    cancelar = Button(ventana3, text='Cancelar compra', 
                      command=lambda: reiniciar_snacks(contador_de_snacks, ventana3, cantidad_visible, ventana_reserva),
                      fg='red', font=15)
    cancelar.pack()
    cancelar.place(x=90, y=250)
 
def botones_snacks(ventana3, informacion_snacks:dict, contador_de_snacks:dict, ventana_reserva, ventana_snacks) -> None:

    encabezado = Label(ventana_snacks, text='COMPRAR SNACKS',
                        fg='white', bg='black')
    encabezado.pack(side='top')

    for snack in informacion_snacks:
        
        posiciones = Frame(ventana3,bg='black')
        posiciones.pack(side='top', anchor='w')

        cantidad_visible = Label(posiciones, text=f'{snack}: {contador_de_snacks[snack]}',
                                 width=15, fg='white', bg='black', font=15)
        cantidad_visible.pack(side='left', 
                              anchor='w')

        restar = Button(posiciones, text='- 1', command=lambda s=snack, c=cantidad_visible: 
                        disminuir_snacks(s, contador_de_snacks, c), fg='red')
        restar.pack(side='left')

        sumar = Button(posiciones, text='+1', command=lambda s=snack, c=cantidad_visible: 
                       aumentar_snacks(s, contador_de_snacks, c), fg='blue')
        sumar.pack(side='left')

        precios = Label(posiciones, text=f'${informacion_snacks[snack]}',
                        width=12, fg='white', bg='black', font=15)
        precios.pack(side='left')
       

    botones_aceptar_cancelar_snacks(ventana3, contador_de_snacks, cantidad_visible, ventana_reserva)


def presentar_cant_entradas(asientos_disponibles_en_la_sala:int) -> str:

    return f'''Hay {asientos_disponibles_en_la_sala} asientos disponibles
Cantidad de entradas a comprar:'''


def validar_texto(nuevo_valor:str) -> bool:

    return nuevo_valor.isdigit() or nuevo_valor == ''


def mostrar_cantidad_de_asientos_disponibles(ventana_reserva, asientos_disponibles_en_la_sala:int) -> None:

    comprar_entradas = Label(ventana_reserva, text='SECCION DE RESERVAS', 
                             fg='white', bg='black', font=15)
    comprar_entradas.pack(pady=5)

    mostrar_cant_asientos = Label(ventana_reserva, fg='white', bg='black', font=15, 
                                  text= presentar_cant_entradas(asientos_disponibles_en_la_sala))
    mostrar_cant_asientos.pack()


def ventana_de_snacks(contador_de_snacks:dict, informacion_snacks:dict, ventana_reserva) -> None:

    ventana_reserva.withdraw()

    ventana_snacks = Toplevel()
    ventana_snacks.geometry('300x300')
    ventana_snacks.config(bg='black')
    ventana_snacks.resizable(width=False, height=False)

    botones_snacks(ventana_snacks, informacion_snacks, contador_de_snacks, ventana_reserva, ventana_snacks)

    ventana_snacks.mainloop()


def ingresar_texto_y_botones(ventana_reserva, ventana_principal, contador_de_snacks:dict, informacion_snacks:dict, 
                             lista_final:list[int], asientos_disponibles_en_la_sala:str, dict_menu:dict, ventana2) -> None:
    
    validar_ingreso = (ventana_reserva.register(validar_texto), '%P')
    eleccion_entradas = Entry(ventana_reserva, width=5, validate="key", validatecommand=validar_ingreso, font=15)
    eleccion_entradas.pack(pady=5)

    opciones_snacks = Button(ventana_reserva, text='Añadir snacks', 
                             fg='green', bg='black', font=15, 
                             command=lambda: ventana_de_snacks(contador_de_snacks, informacion_snacks, 
                                                               ventana_reserva))
    opciones_snacks.pack(pady=5)

    terminar_compra = Button(ventana_reserva, text='Ir a Carrito', 
                             fg='blue', bg='black', font=15, 
                             command=lambda: confirmar_compra(informacion_snacks, contador_de_snacks,
                                                             asientos_disponibles_en_la_sala, lista_final, 
                                                             ventana_reserva, dict_menu, eleccion_entradas, 
                                                             ventana_principal))
    terminar_compra.pack(pady=5)

    cancelar = Button(ventana_reserva, text='Cancelar compra', 
                      fg='red', bg='black', font=15, 
                      command=lambda: cancelar_compra(ventana2, ventana_reserva))
    cancelar.pack(pady=5)

    
def advertencia_sin_asientos(ventana_anterior) -> None:

    ventana_anterior.withdraw()
    messagebox.showwarning('Advertencia', 'Ya no hay asientos disponibles')
    ventana_anterior.deiconify()


def ejecutar_ventana_de_reservas(ventana_anterior, asientos_disponibles_en_la_sala:int, dict_menu:dict, ventana_principal) -> None:
        
    ventana_anterior.withdraw()

    lista_final: list =[]
    informacion_snacks: dict = obtener_snacks()
    contador_de_snacks: dict = {}
    cantidad_de_snacks(informacion_snacks, contador_de_snacks)

    ventana_reserva = Toplevel()
    ventana_reserva.geometry('300x250')
    ventana_reserva.title('')
    ventana_reserva.resizable(width=False, height=False)
    ventana_reserva.config(bg='black')

    mostrar_cantidad_de_asientos_disponibles(ventana_reserva, asientos_disponibles_en_la_sala)
    ingresar_texto_y_botones(ventana_reserva, ventana_principal, contador_de_snacks, informacion_snacks, lista_final,
                        asientos_disponibles_en_la_sala, dict_menu, ventana_anterior)
        

def ventana_de_reservas(ventana2, dict_menu:dict, asientos_disponibles_en_la_sala:str, ventana_principal) -> None:

    if asientos_disponibles_en_la_sala == NO_HAY_ASIENTOS_DISPONIBLES:
        advertencia_sin_asientos(ventana2)

    else:
        ejecutar_ventana_de_reservas(ventana2, asientos_disponibles_en_la_sala, dict_menu, ventana_principal)


#-------------------------------------FUNCIONES_PARA_LA_VENTANA_QUE_MUESTRA_LA_INFORMACION_DE_LA_PELICULA_SELECCIONADA------------------------------------------


def api_ventana_secundaria(id_principal:str) -> tuple[str]:

    guardar: list = []

    url = "http://vps-3701198-x.dattaweb.com:4000/movies/" + id_principal
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == ACEPTADO:
        diccionario_informacion = verificar_archivo.json()

    informacion = list(diccionario_informacion.keys())

    for linea in range(INICIAL, FINAL): 
        variable = diccionario_informacion[informacion[linea]] 
        guardar.append(variable)

    return id_principal, guardar


def volver_al_menu(ventana_secundaria, ventana_principal) -> None:

    ventana_principal.iconify()
    ventana_principal.deiconify()
    ventana_secundaria.destroy()


def botones_reserar_o_regresar(ventana_secundaria, ventana_principal, dict_menu:dict, asientos_disponibles_en_la_sala:str) -> None:

    boton_volver_al_menu = Button(ventana_secundaria,  text= "VOLVER AL MENU", 
                                 background= "black",  fg="gold", 
                                 width= 20,           height= 5, 
                                 command= lambda: volver_al_menu(ventana_secundaria,ventana_principal))
    boton_volver_al_menu.place(relx=0.1, rely=0.1, anchor=CENTER)

    boton_reservar = Button(ventana_secundaria,  text= "RESERVAR", 
                            background= "black",  fg="blue",  
                            width= 20,          height= 5,
                            command= lambda: ventana_de_reservas(ventana_secundaria, dict_menu, 
                                                                 asientos_disponibles_en_la_sala, ventana_principal))
    boton_reservar.place(relx=0.88, rely=0.9, anchor=CENTER)


def sala(ventana_secundaria, id:str) -> None:

    sala_proyectar = Label(ventana_secundaria,   text= "SALA  " + id,
                            background= "black",  fg="red")
    sala_proyectar.place(relx=0.5, rely=0.1, anchor=CENTER)


def sinopsis(ventana_secundaria, guardar:list[str]) -> None: 

    sinopsis = Label(ventana_secundaria, text= "SINOPSIS: ",
                     background= "black", fg="red")
    sinopsis.place(relx=0.2, rely=0.3, anchor=CENTER)

    texto_sinopsis = Label(ventana_secundaria,   text= guardar[INFO_SINOPSIS],
                           background= "black",  fg="red",    
                           wraplength= 700)
    texto_sinopsis.place(relx=0.5, rely=0.42, anchor=CENTER)


def genero(ventana_secundaria, guardar:list[str]) -> None:

    genero = Label(ventana_secundaria,    text= "GENERO: ",
                   background= "black",   fg="red")
    genero.place(relx=0.2, rely=0.55, anchor=CENTER)

    texto_genero = Label(ventana_secundaria,    text= guardar[INFO_GENERO_PELICULA],
                         background= "black",   fg="red")  
    texto_genero.place(relx=0.25, rely=0.55, anchor=CENTER)


def duracion(ventana_secundaria, guardar:list[str]) -> None:

    duracion = Label(ventana_secundaria, text= "DURACION: ",
                    background= "black", fg="red")
    duracion.place(relx=0.2, rely=0.6, anchor=CENTER)

    texto_duracion = Label(ventana_secundaria,  text= guardar[INFO_DURACION_PELICULA],
                           background= "black", fg="red")
    texto_duracion.place(relx=0.25, rely=0.6, anchor=CENTER)
    

def actores(ventana_secundaria, guardar:list[str]) -> None:

    actores = Label(ventana_secundaria, text= "ACTORES: ",
                    background= "black", fg="red")
    actores.place(relx=0.2, rely=0.66, anchor=CENTER)

    texto_actores = Label(ventana_secundaria, text= guardar[INFO_ACTORES],
                          background= "black", fg="red")
    texto_actores.place(relx=0.35, rely=0.66, anchor=CENTER)


def obtener_cantidad_asientos(dict_menu:dict) -> int:
    
    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == ACEPTADO:
        lista_de_cinemas = verificar_archivo.json()

        for informacion_cinemas in lista_de_cinemas:
            if informacion_cinemas['location'] == dict_menu['location']:
                return informacion_cinemas['available_seats'] 
            

def saber_asientos_comprados_de_cada_pelicula() -> dict:
    
    ruta_ingresos:str = 'ingresos.txt'
    informacion_asientos_comprados:dict = {}

    if path.exists(ruta_ingresos):
        with open(ruta_ingresos, 'r') as archivo_ingesos:
            for linea in archivo_ingesos:
                datos = linea.strip('\n').split(', ')
                cinema = datos[NOMBRE_CINEMA]
                pelicula = datos[NOMBRE_PELICULA]
                entradas_vendidas = int(datos[CANT_ENTRADAS_VENDIDAS])
                if cinema not in informacion_asientos_comprados:
                    informacion_asientos_comprados[cinema] = {}
                if pelicula in informacion_asientos_comprados[cinema]:
                    informacion_asientos_comprados[cinema][pelicula] += entradas_vendidas
                else:
                    informacion_asientos_comprados[cinema][pelicula] = entradas_vendidas

    return informacion_asientos_comprados


def asientos_comprados_en_la_sala(dict_menu:dict, dict_del_txt:dict) -> int:

    letra_español:str = 'Ñ'
    conversion_de_letra:str = 'NI'

    location = dict_menu['location']
    name = dict_menu['name']

    if letra_español in name:
        name = name.replace(letra_español, conversion_de_letra)
    
    if location in dict_del_txt and name in dict_del_txt[location]:
        return dict_del_txt[location][name]
    
    else:
        return 0


def obtener_asientos_disponibles(dict_menu:dict) -> int:

    asientos_totales:int = obtener_cantidad_asientos(dict_menu)
    dict_del_txt:dict = saber_asientos_comprados_de_cada_pelicula()
    asientos_reservados:int = asientos_comprados_en_la_sala(dict_menu, dict_del_txt)
    asientos_disponibles:int = asientos_totales - asientos_reservados

    return asientos_disponibles


def ventana_informacion_pelicula(dict_menu:dict , ventana_principal) -> None:

    asientos_disponibles_en_la_sala:int = obtener_asientos_disponibles(dict_menu)

    print(f'asientos disponibles: {asientos_disponibles_en_la_sala}')

    ventana_principal.withdraw()
    id_principal = dict_menu["id"]
    id, guardar = api_ventana_secundaria(id_principal)

    ventana_secundaria = Toplevel()
    ventana_secundaria.title("ventana secundaria")
    ventana_secundaria.geometry("1150x500")
    ventana_secundaria.config(background="black")
    ventana_secundaria.resizable(width=False, height=False)
   
    botones_reserar_o_regresar(ventana_secundaria,ventana_principal,dict_menu,asientos_disponibles_en_la_sala)
    sala(ventana_secundaria, id)
    sinopsis(ventana_secundaria, guardar)
    genero(ventana_secundaria, guardar)
    actores(ventana_secundaria, guardar)
    duracion(ventana_secundaria,guardar)

    ventana_secundaria.mainloop()


#-----------------------------------------------------FUNCIONES_PARA_LA_VENTANA_PRINCIPAL-----------------------------------------------------------#


def boton_peliculas(sub_id:int, ventana, id_cine, nombre_cine) -> None:

    url = "http://vps-3701198-x.dattaweb.com:4000/movies/" + str(sub_id)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    informacion_de_movies = get(url, headers=headers)

    if informacion_de_movies.status_code == ACEPTADO:
        
        archivo = informacion_de_movies.json() 
        id = archivo["id"]
        nombre = archivo["name"]
        diccionario : dict = {"name": nombre, "id": id , "cinema_id": id_cine, "location": nombre_cine}
        ventana_informacion_pelicula(diccionario,ventana)
    

def lista_posters(sub_lista:str) -> str:

    url = "http://vps-3701198-x.dattaweb.com:4000/posters/" + str(sub_lista)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'}
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == ACEPTADO:
        datos = verificar_archivo.json()
       
        for i in datos:
            variable = datos[i]

            return variable
    

def lista_peliculas(id:str) -> list:

    sub_lista : list = []
    
    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas/{0}/movies".format(id)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    verificar_archivo = get(url, headers=headers)

    if verificar_archivo.status_code == ACEPTADO:
        datos = verificar_archivo.json() #diccionario
        
        for i in datos:
            variable = i["has_movies"]
            sub_lista += variable

    return sub_lista


def mensaje_no_se_encontro_pelicula() -> None:

    sub_ventana = Toplevel()
    sub_ventana.geometry("300x200")
    sub_ventana.title("ERROR !!!")

    sub_frame = Frame(sub_ventana,bg="black")
    sub_frame.pack(expand=True,fill="both")

    mensaje = Label(sub_frame, text="NO SE ENCONTRO LA PELICULA. INTENTE DE NUEVO",
                    bg="black", fg="red")
    mensaje.pack(ipadx=50,ipady=50)

    sub_boton = Button(sub_frame, text = "OK",
                        command=sub_ventana.destroy, 
                        bg="black",fg="red")
    sub_boton.pack(ipadx=25,ipady=10)


def mostrar_pelicula_buscado_textualmente(lista_completa:list[str], datos:str, id:str, 
                                          id_cinema:str, nombre_locacion:str, ventana) -> None:

    for sub_vueltas in lista_completa:
        if datos == sub_vueltas["name"]:
            id = sub_vueltas["id"]
            diccionario : dict = {"name" : datos ,"id" : id , "cinema_id": id_cinema,"location": nombre_locacion}
            ventana_informacion_pelicula(diccionario, ventana)



def buscar(cajon, ventana, sub_lista_de_peliculas:list, id_cinema:str, nombre_locacion:str) -> None:

    '''
    PRE-CONDICION: PARA QUE FUNCIONE LA BÚSQUERA, ES INDISPENSABLE QUE INGRESE EL
                   NOMBRE COMPLETO DE LA MISMA
    PORT-CONDICION: MANDARÁ A LA SIGUIENTE VENTANA CON LA INFORMACION DE AQUELLA PELICULA
    '''

    datos = cajon.get().upper()

    lista_de_peliculas : list = []
    lista_completa : list = []
    
    for vueltas in sub_lista_de_peliculas:
        url = "http://vps-3701198-x.dattaweb.com:4000/movies/{0}".format(vueltas)
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

        headers = {'Authorization': f'Bearer {token}'} #llave de acceso
        verificar_archivo = get(url, headers=headers)

        if verificar_archivo.status_code == ACEPTADO:
            archivo = verificar_archivo.json()
            lista_de_peliculas.append(archivo["name"])
            lista_completa.append(archivo) 

    if datos in lista_de_peliculas:
        mostrar_pelicula_buscado_textualmente(lista_completa, datos, id, id_cinema, 
                                              nombre_locacion, ventana)

    else:
        mensaje_no_se_encontro_pelicula()


def crear_boton_pelicula(numero_id:str, nombre_cine:str, sub_frame, imagen, 
                         pelicula_info:str, ventana, contar_peliculas:int) -> None:

    fila:int = contar_peliculas // 2
    columna:int =contar_peliculas % 2

    boton_pelicula = Button(sub_frame, image=imagen, bg="black",
                            command=lambda info=pelicula_info:  
                            boton_peliculas(info, ventana,numero_id,nombre_cine))
    boton_pelicula.grid(row=fila, column=columna)


def cargar_imagen_pelicula(pelicula_info:str) -> str:

    funcion_pelicula: str = lista_posters(pelicula_info) 
    base64_data_pelicula: str = funcion_pelicula.split(",")[1]  
    imagen_a_deco_pelicula: bytes = b64decode(base64_data_pelicula)
    imagen_capturada_pelicula = ImageTk.PhotoImage(data=imagen_a_deco_pelicula)

    return imagen_capturada_pelicula  


def configurar_frame_canvas_scrollbar(ventana, side:str)-> tuple:

    frame = Frame(ventana,     bg="black",
                  height=1000, width=600,
                  relief="raised", bd=25)
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


def ejecucion_boton_pelicula(listas_de_peliculas:list[str], ventana, cine_numero:str, nombre_cine:str) -> list[str]:

    sub_frame_1: tuple = configurar_frame_canvas_scrollbar(ventana, "left")
    sub_frame_2: tuple = configurar_frame_canvas_scrollbar(ventana, "right")
    
    lista_imagenes: list = []
    cantidad_peliculas:int = len(listas_de_peliculas)

    corte:int = 5

    for contar_peliculas in range(cantidad_peliculas):
        pelicula_info = listas_de_peliculas[contar_peliculas]
        
        imagen_pelicula = cargar_imagen_pelicula(pelicula_info)
        lista_imagenes.append(imagen_pelicula)

        if contar_peliculas <= corte:
            sub_frame = sub_frame_1
        else:
            sub_frame = sub_frame_2

        crear_boton_pelicula(cine_numero, nombre_cine, sub_frame, 
                             imagen_pelicula, pelicula_info, 
                             ventana, contar_peliculas)
    
    return lista_imagenes

def volver_elegir_cine(pantalla_actual) -> None:

    pantalla_actual.destroy()
    menu_cines()


def ventana_principal(numero_cine:str, nombre_cine:str, ventana_anterior) -> None:

    '''
    PRE-CONDICION: APRETAR CUALQUIER PERLICULA O EL NOMBRE COMPLETA EN LA BARRA DE BÚSQUERA
    POST-CONDICION: SE ABRIRÁ LA SIGUIENTE VENTANA LA CUAL TENDRÁ LA INFORMACIÓN DE LA
                    PELICULA SELECCIONADA
    '''
    
    ventana_anterior.destroy()

    ventana = Tk()
    ventana.geometry("960x500")
    ventana.title("TOTEM CINEMA")
    ventana.resizable(width=False, height=False)

    fram_1 = Frame(ventana, bg="black", relief="raised", bd=25)
    fram_1.pack(fill="x")

    cajon = Entry(fram_1)
    cajon.grid(row=0, column=0, ipadx=100, ipady=5)

    listas_de_peliculas:list[str] = lista_peliculas(numero_cine)

    boton_busqueda = Button(fram_1, text="BUSCAR",
                            command=lambda: buscar(cajon, ventana, listas_de_peliculas, numero_cine,nombre_cine),
                            bg="black", fg="red")
    boton_busqueda.grid(row=0, column=1, padx=60, ipadx=30, ipady=5)

    ubicacion = Button(fram_1, text=f"CINE : {nombre_cine}", command=lambda: volver_elegir_cine(ventana), 
                        bg="black", fg="red")
    ubicacion.grid(row=0, column=2, padx=150, ipadx=30, ipady=5)

    imagen_ejecutable:list = ejecucion_boton_pelicula(listas_de_peliculas, ventana, numero_cine, nombre_cine)

    ventana.mainloop()


#-------------------------------------------------------FUNCIONES_PARA_LA_VENTANA_DE_ELEGIR_CINE-----------------------------------------------------#


def crear_boton_cines(frame, cine_id:str, nombre_cine:str, ventana) -> None:

    boton_1 = Button(frame, text=nombre_cine, bg="black", 
                     fg="gold", width=30, height=2, font=("Helvetica", 13), 
                     command=lambda : ventana_principal(cine_id,nombre_cine,ventana)) 
    boton_1.pack(pady=5)


def cinemas() -> tuple[str]:

    lista_id:list = []
    nombre_cine:list = []

    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"

    headers = {'Authorization': f'Bearer {token}'} #llave de acceso
    response__1 = get(url, headers=headers)

    if response__1.status_code == ACEPTADO:
        datos = response__1.json() #diccionario

        for i in datos:
            lista_id.append(i["cinema_id"])
            nombre_cine.append(i["location"])

    return lista_id , nombre_cine


def menu_cines() -> None:
    '''
    PRE-CONDICION: SI QUEREMOS SALIR DE LA APLICACION, UNICAMENTE CERRAR LA VENTANA, YA SEA ESTA O
                   LA SIGUIENTE (TRAS HABER APRETADO EL CINE), DONDE SE MUESTRAN LAS PELICULAS
    POS-CONDICION: SE CERRARÁ EL PROGRAMA CORRECTAMENTE
    '''
    ventana = Tk()
    ventana.geometry("230x436")
    ventana.title("MENU")
    ventana.resizable(width=False, height=False)

    frame = Frame(ventana, bg="black")
    frame.pack(expand=True, fill="both")

    cine_id, nombre_cine = cinemas()
    numero:int=0

    for vueltas in range(len(cine_id)):
        crear_boton_cines(frame,cine_id[numero],nombre_cine[numero],ventana)
        numero += 1

    ventana.mainloop()



#----------------------------------------------------------------------APP_QR---------------------------------------------------------------------#


def extraer_imagen_desde_pdf(archivo_pdf:str, ruta_imagen_png:str) -> bool:

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
    

def decodificar_qr_desde_imagen(ruta_imagen:str) -> str:

    '''
    PRE-CONDICION: MOSTRAR SOLO CODIGO QR PROPORCIONADO POR LA APP
    POST-CONDICION: SE DEVUELVE TODA LA CADENA DE INFORMACION DEL QR
    '''

    imagen = imread(ruta_imagen)
    imagen_gris = cvtColor(imagen, COLOR_BGR2GRAY)
    detector = QRCodeDetector()
    datos_qr = detector.detectAndDecode(imagen_gris)


    return datos_qr[0]


def agregar_a_ingresos_txt(codigo_qr:str) -> None:

    with open("ingresos.txt", "a") as archivo_ingresos:
        archivo_ingresos.write(f'{codigo_qr}\n')


def generar_ventana_emergente(mensaje:int) -> None:

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


def codigo_por_texto(cajon) -> None:

    '''
    PRE-CONDICION: INGRESAR CODIGOS QUE INICIEN CON 'QR_(VALOR NUMERICO)'
    POST-CONDICION: INGRESARÁ LA INFORMACION DEL QR EN INGRESOS.TXT
    '''

    carpeta_pdf:str = 'QR'

    ruta_ingresos:str = 'ingresos.txt'
    dato_entrada = cajon.get().upper()

    archivo_pdf = f"{dato_entrada}.pdf"
    ruta_completa_pdf = path.join(carpeta_pdf, archivo_pdf)

    if path.exists(ruta_completa_pdf):
        ruta_imagen_png = path.join(carpeta_pdf, f'{dato_entrada}.png')

        if extraer_imagen_desde_pdf(ruta_completa_pdf, ruta_imagen_png):
            codigo_qr = decodificar_qr_desde_imagen(ruta_imagen_png)

            with open(ruta_ingresos, "a+") as archivo_lectura:
                archivo_lectura.seek(0)
                contenido_actual = archivo_lectura.read()

            if codigo_qr is not None:
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

    try:
        if path.exists(ruta_imagen_png):
            remove(ruta_imagen_png)

    except UnboundLocalError:
        mensaje = "NO EXISTE LA CARPETA 'QR'"
        generar_ventana_emergente(mensaje)


def guardar_informacion_QR_en_ingresos(dato_qr:str)->None:
    
    '''
    PRE-CONDICION: VERIFICARÁ SI EL CODIGO ES NUEVO O YA ESTÁ GUARDADO EN INGRESOS.TXT
    POST-CONDICION: GUARDARÁ Y/O GENERARÁ CUADRO DE MENSAJE DEPENDIENDO
    '''

    ruta_ingresos:str = 'ingresos.txt'

    with open(ruta_ingresos, "a+") as archivo_lectura:
        archivo_lectura.seek(0)
        contenido_actual = archivo_lectura.read()

    if dato_qr not in contenido_actual:
        with open(ruta_ingresos, "a") as archivo:
            archivo.write(dato_qr + '\n')
        mensaje = "SE REGISTRO CORRECTAMENTE EL QR"
        generar_ventana_emergente(mensaje)

    elif dato_qr in contenido_actual:
        mensaje = "CÓDIGO YA REGIDSTRAO"
        generar_ventana_emergente(mensaje)

    else:
        mensaje = "CÓDIGO INVALIDO"
        generar_ventana_emergente(mensaje)


def lector_qr() -> None:

    '''
    PRE_CONDICION: MOSTRAR SOLO CÓDIGOS QUE SE HAYAN CREADO CON NUESTRA APP DE CINES
    POST_CONDICION: GUARDARÁ TODA LA INFORMACION DEL QR EN INGRESOS.TXT
    '''

    camara = VideoCapture(0)
    ciclo = True
    dato_qr = ""

    while ciclo:
        ret, frame = camara.read()

        if waitKey(1) & 0xFF == ord("s"):
            ciclo = False

        detector = QRCodeDetector()
        data, bbox, rectifiedImage = detector.detectAndDecode(frame)

        if len(data) > 0:
            imshow("web", rectifiedImage)
            dato_qr = data
            ciclo = False

        else:
            imshow("web", frame)

    camara.release()
    destroyAllWindows()

    guardar_informacion_QR_en_ingresos(dato_qr)


def menu_QR():
    
    '''
    PRE-CONDICION: CERRAR LA VENTANA UNICAMENTE CUANDO EL LECTOR NO ESTÉ FUNCIONANDO
    POR-CONDICION: NO HABRÁ POSIBLE PROBLEMAS 
    '''
    ventana_qr = Tk()
    ventana_qr.geometry("530x300")
    ventana_qr.title("Validacion")
    ventana_qr.resizable(width=False, height=False)


    frame_principal = Frame(ventana_qr, bg="black")
    frame_principal.pack(expand=True, fill="both")

    label_1 = Label(frame_principal, text="INGRESE SU CODIGO", font=("Helvetica", 15))
    label_1.config(bg="black", fg="red")
    label_1.pack(pady=20, ipadx=50, ipady=5)

    cajon = Entry(frame_principal)
    cajon.pack(pady=20, ipadx=50)

    boton_1 = Button(frame_principal, text="LEER QR POR TEXTO", command=lambda: codigo_por_texto(cajon))
    boton_1.config(bg="black", fg="red")
    boton_1.pack(pady=20, ipadx=50, ipady=2)

    boton_2 = Button(frame_principal, text="LEER QR", command=lambda: lector_qr())
    boton_2.config(bg="black", fg="red")
    boton_2.pack(pady=20, ipadx=50, ipady=5)

#------------------------------------------------------------MENU/OPCION-------------------------------------------------------------------------#

def menu() -> str:

    '''
    PRE-CONDICION: NO ABRIR LAS 2 APPS AL MISMO TIEMPO
    POST-CONDICION: EL PROGRAMA CORRERÁ SIN PROBLEMAS
    '''
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
            menu_cines()
        elif respuesta == '2':
            menu_QR()
        elif respuesta == '3':
            sigamos: bool = False

main()
#ventana
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



    lista_de_posters : list = lista_posters(listas_de_peliculas)

    url = "http://vps-3701198-x.dattaweb.com:4000/cinemas/1/movies"
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.DGI_v9bwNm_kSrC-CQSb3dBFzxOlrtBDHcEGXvCFqgU"



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
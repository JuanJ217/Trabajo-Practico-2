from tkinter import Entry, Button, Label, Tk

def ventana_prueba()->None:

    ventana = Tk()
    ventana.geometry('300x150')
    ventana.title('')
    ventana.resizable(width=False, height=False)

    comprar_entradas = Label(ventana, text='SECCION DE RESERVAS')
    comprar_entradas.pack()

    for opciones in range(1):
        entrada = Label(ventana, text='Cantidad de entradas')
        entrada.pack()
        entrada.place(x=20, y=20)

        opciones_snacks = Button(ventana, text='Añadir snacks')
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

    ventana.mainloop()

def main():
    ventana_prueba()
main()
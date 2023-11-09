from tkinter import Tk, Button, Label, Frame

def cantidad_de_click(lista_de_click, contador_de_click):
    for elemento in lista_de_click:
        contador_de_click[elemento] = 0

def aumentar(elemento, contador_de_click, label):
    contador_de_click[elemento] += 1
    label.config(text=f'{elemento} {contador_de_click[elemento]}')

def disminuir(elemento, contador_de_click, label):
    if contador_de_click[elemento] > 0:
        contador_de_click[elemento] -= 1
        label.config(text=f'{elemento} {contador_de_click[elemento]}')

def ventana_de_prueba(contador_de_click):
    ventana = Tk()
    ventana.geometry('200x200')

    for elemento in contador_de_click:
        frame = Frame(ventana)
        frame.pack(side='top', anchor='w')

        label = Label(frame, text=f'{elemento} {contador_de_click[elemento]}')
        sumar = Button(frame, text='+1', command=lambda e=elemento, l=label: aumentar(e, contador_de_click, l))
        restar = Button(frame, text='-1', command=lambda e=elemento, l=label: disminuir(e, contador_de_click, l))
        
        label.pack(side='left', anchor='w')
        sumar.pack(side='left')
        restar.pack(side='left')

    ventana.mainloop()

def main():
    lista_de_click = ['click 1', 'click 2']
    contador_de_click = {}
    cantidad_de_click(lista_de_click, contador_de_click)
    ventana_de_prueba(contador_de_click)

main()

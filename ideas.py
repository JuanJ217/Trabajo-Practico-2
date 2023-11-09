import tkinter as tk

ventana = tk.Tk()
ventana.title("Botones con Conteo")

# Crear una lista de nombres para los botones
nombres_botones = ["Botón 1", "Botón 2", "Botón 3", "Botón 4"]

# Función que se ejecutará cuando se presione un botón
def boton_presionado(nombre):
    contador_botones[nombre] += 1
    actualizar_botones()

# Función para decrementar el contador
def decrementar_contador(nombre):
    if contador_botones[nombre] > 0:
        contador_botones[nombre] -= 1
        actualizar_botones()

# Función para mostrar la información en una ventana
def mostrar_informacion():
    info_ventana = tk.Toplevel(ventana)
    info_ventana.title("Información de Botones")

    lista_informacion = [f"{nombre}: {contador_botones[nombre]}" for nombre in nombres_botones]

    lista_texto = tk.Label(info_ventana, text="\n".join(lista_informacion))
    lista_texto.pack()

# Crear y configurar los botones en un bucle
contador_botones = {nombre: 0 for nombre in nombres_botones}
botones = {}

def actualizar_botones():
    for nombre in nombres_botones:
        botones[nombre].config(text=f"{nombre} ({contador_botones[nombre]})")

for nombre in nombres_botones:
    boton = tk.Label(ventana, text=f"{nombre} (0)", width=20, height=2)
    boton.pack(side="left", padx=5)
    botones[nombre] = boton

    boton_mas = tk.Button(ventana, text="+", command=lambda n=nombre: boton_presionado(n))
    boton_mas.pack(side="left")
    
    boton_menos = tk.Button(ventana, text="-", command=lambda n=nombre: decrementar_contador(n))
    boton_menos.pack(side="left")

# Crear un botón para mostrar la información
boton_info = tk.Button(ventana, text="Mostrar Información", command=mostrar_informacion)
boton_info.pack()

ventana.mainloop()

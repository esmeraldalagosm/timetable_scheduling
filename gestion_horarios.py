"""
#####    datos de entrada
1. Tabla .csv: [ Materia | Sección | Día | Timeslot ] --> una entrada por cada clase 
2. Lista de materias a las que me quiero inscribir = lista de strings

####     quiero
1. poder agarrar las materias a las que me quiero inscribir (y sus secciones)
2. obetener las combinaciones de secciones que no se superpongan
"""

import csv
from seccion import Seccion
from collections import defaultdict
from itertools import product
import tkinter as tk


#carga de datos. Armo Secciones de las materias a las que me quier inscribir
def upload_sections(path_csv, wanted_classes):
    """
    La función lee un archivo CSV que contiene información sobre 
    secciones de materias y sus horarios, y crea una lista de objetos Seccion organizados correctamente (siempre y cuando me interese esa materia).
    wanted_clases es una lista de materias (solo nombre)
    """
    secciones_temp = defaultdict(list)  # {(materia, comision_id): [(dia, timeslot), ...]}
    """
    Es una estructura de datos de Python (de collections) que se comporta como un diccionario normal, 
    pero si accedés a una clave que no existe, automáticamente la crea con una lista vacía.
    """

    with open(path_csv, newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            materia = fila["Materia"]
            if materia in wanted_classes:
                seccion_id = int(fila["Sección"])
                dia = fila["Día"].strip()
                timeslot = int(fila["Timeslot"])
                secciones_temp[(materia, seccion_id)].append((dia, timeslot))

        secciones = []
        for (materia, seccion_id), horarios in secciones_temp.items():
            secciones.append(Seccion(materia, seccion_id, horarios))

        return secciones 
    """
    lista de las secciones posibles para todas las materias a las que me quiero inscribir. 
    una seccion es de la forma:
    { "Álgebra", 1, [("Lunes", 1), ("Miércoles", 3)] } 
    { materia, seccion, lista de tuplas (dia, horario)}
    """       
    

def hay_superposicion(combinacion) -> bool:
    """
    TRUE si los horarios de alguna seccion en esa combinacion se superponen
    FALSE caso contrario
    """
    timeslot_ocupados = set()
    for seccion in combinacion:
        for horario in seccion.horarios:
            if horario in timeslot_ocupados:
                return True
            timeslot_ocupados.add(horario)
    return False

#Ahora armo las combinaciones que no se superpongan. Fuerza bruta + backtraking? 
def generar_timetables_validos(path_csv, wanted_classes):
    opciones_secciones = upload_sections(path_csv, wanted_classes)
    # En opciones_secciones tengo una lista de todas las secciones a las que me puedo inscribir.
    """
    IDEA: agrupar las secciones en opciones_secciones por materia, y dsps usar el producto cartesiano. 
    """
    # Agrupo secciones por materia
    opciones_por_materia = defaultdict(list)
    for seccion in opciones_secciones:
        opciones_por_materia[seccion.materia].append(seccion)
    ## diccionario de la forma: [Materia, secciones disponibles]

    # Me aseguro de tener una sección para cada materia deseada
    if set(opciones_por_materia.keys()) != set(wanted_classes):
        print("Faltan secciones para algunas materias.")
        return []
    
    # Creo combinaciones de 1 sección por materia
    combinaciones_posibles = product(*[opciones_por_materia[m] for m in wanted_classes])
    """
    [opciones_por_materia[m] for m in wanted_classes] --> lista de listas. 
        en la posicion i tengo una lista de las secciones disponibles para la materia i
    el * desempaqueta la lista: pasan a ser listas separadas
    product(lista1, lista2, lista3,...) --> geera todas las combinaciones posibles tomando una seccion por materia (= un elemento por lista
    )
    """
    # ahora en combinaciones_posibles tengo un iterador de tuplas de objetos de tipo Sección.
    # lo puedo recorrer una vez

    # Filtro las combinaciones que no tienen superposición
    combinaciones_validas = []
    for comb in combinaciones_posibles: #comb es tupla de una Seccion x materia
        if not hay_superposicion(comb):
            combinaciones_validas.append(comb)

    return combinaciones_validas


archivo = "data_prueba.csv" ### COMPLETAR CON ARCHIVO PROPIO (respetar formato)
quiero = ["Algebra", "Matemática"] ### COMPLETAR CON LISTA DE MATERIAS
timetables = generar_timetables_validos(archivo, quiero)
print(timetables)

# -----------------------------------
# INTERFAZ con Tkinter


dias = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes"] 
timeslots = [1, 2, 3, 4, 5]
colores = ["#AEC6CF", "#FFB347", "#B39EB5", "#77DD77", "#FF6961", "#FDFD96"] #asumiendo que nunca me anoto en más de 6 materias. 
"""
quiero[i] corresponde a colores[i]
"""
root = tk.Tk()
root.title("Generador de Horarios")

# Etiquetas días
for col, dia in enumerate(dias, start=1):
    tk.Label(root, text=dia, borderwidth=1, relief="solid", width=12).grid(row=0, column=col)

# Etiquetas timeslots
for row, ts in enumerate(timeslots, start=1):
    tk.Label(root, text=f"Slot {ts}", borderwidth=1, relief="solid", width=10).grid(row=row, column=0)

# Contenedor para las etiquetas de materias
celdas = {}


def mostrar_combinacion(index):
    # Limpiar etiquetas previas
    for label in celdas.values():
        label.destroy()
    celdas.clear()

    if index < 0 or index >= len(timetables):
        return

    combinacion = timetables[index]
    root.title(f"Generador de Horarios - Combinación {index+1} de {len(timetables)}")

    # Crear dict para fácil acceso (dia, timeslot) -> materia+sección
    horario = {}
    for seccion in combinacion:
        for dia, ts in seccion.horarios:
            horario[(dia, ts)] = f"{seccion.materia} S{seccion.seccion_id}"
    # Pintar en grid
    for (dia, ts), texto in horario.items():
        col = dias.index(dia) + 1
        row = ts
        
        materia = texto.split(" S")[0]
        k = quiero.index(materia)

        label = tk.Label(root, text=texto, bg=colores[k], borderwidth=1, relief="solid", width=12)
        label.grid(row=row, column=col, sticky="nsew")
        celdas[(row, col)] = label
        

# Variables para controlar índice
indice_actual = 0

# Botones para navegar
def anterior():
    global indice_actual
    if indice_actual > 0:
        indice_actual -= 1
        mostrar_combinacion(indice_actual)

def siguiente():
    global indice_actual
    if indice_actual < len(timetables) - 1:
        indice_actual += 1
        mostrar_combinacion(indice_actual)

btn_anterior = tk.Button(root, text="Anterior", command=anterior)
btn_anterior.grid(row=len(timeslots)+1, column=0, columnspan=2, sticky="ew")

btn_siguiente = tk.Button(root, text="Siguiente", command=siguiente)
btn_siguiente.grid(row=len(timeslots)+1, column=3, columnspan=3, sticky="ew")

# Mostrar la primera combinacion
mostrar_combinacion(indice_actual)

root.mainloop()


#correr con python3 prueba_interfaz.py

import tkinter as tk
from collections import defaultdict
from itertools import product

# -----------------------------------
# Simulo la clase Seccion para ejemplo
class Seccion:
    def __init__(self, materia, seccion_id, horarios):
        self.materia = materia
        self.seccion_id = seccion_id
        self.horarios = horarios

    def __repr__(self):
        return f"{self.materia} S{self.seccion_id}"


# -----------------------------------
# Funciones para simular combinaciones válidas

def se_superponen(combinacion):
    ocupados = set()
    for seccion in combinacion:
        for horario in seccion.horarios:
            if horario in ocupados:
                return True
            ocupados.add(horario)
    return False

def generar_combinaciones_validas(opciones_por_materia):
    todas_combinaciones = product(*opciones_por_materia.values())
    combinaciones_validas = [c for c in todas_combinaciones if not se_superponen(c)]
    return combinaciones_validas


# -----------------------------------
# Datos de ejemplo: materias y secciones
opciones_por_materia = {
    "Álgebra": [
        Seccion("Álgebra", 1, [("Lunes", 1), ("Miércoles", 2)]),
        Seccion("Álgebra", 2, [("Martes", 1), ("Jueves", 3)])
    ],
    "Programación": [
        Seccion("Programación", 1, [("Lunes", 2), ("Viernes", 3)]),
        Seccion("Programación", 2, [("Martes", 3), ("Jueves", 1)])
    ],
    "Análisis": [
        Seccion("Análisis", 1, [("Miércoles", 1), ("Viernes", 2)]),
        Seccion("Análisis", 2, [("Jueves", 2), ("Viernes", 1)])
    ],
}

combinaciones = generar_combinaciones_validas(opciones_por_materia)


# -----------------------------------
# INTERFAZ con Tkinter

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
timeslots = [1, 2, 3, 4, 5]

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

    if index < 0 or index >= len(combinaciones):
        return

    combinacion = combinaciones[index]
    root.title(f"Generador de Horarios - Combinación {index+1} de {len(combinaciones)}")

    # Crear dict para fácil acceso (dia, timeslot) -> materia+sección
    horario = {}
    for seccion in combinacion:
        for dia, ts in seccion.horarios:
            horario[(dia, ts)] = f"{seccion.materia} S{seccion.seccion_id}"

    # Pintar en grid
    for (dia, ts), texto in horario.items():
        col = dias.index(dia) + 1
        row = ts
        label = tk.Label(root, text=texto, bg="lightblue", borderwidth=1, relief="solid", width=12)
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
    if indice_actual < len(combinaciones) - 1:
        indice_actual += 1
        mostrar_combinacion(indice_actual)

btn_anterior = tk.Button(root, text="Anterior", command=anterior)
btn_anterior.grid(row=len(timeslots)+1, column=0, columnspan=2, sticky="ew")

btn_siguiente = tk.Button(root, text="Siguiente", command=siguiente)
btn_siguiente.grid(row=len(timeslots)+1, column=3, columnspan=3, sticky="ew")

# Mostrar la primera combinacion
mostrar_combinacion(indice_actual)

root.mainloop()
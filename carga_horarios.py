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

    with open("comisiones.csv", newline='') as archivo:
        lector = csv.DictReader(archivo)
        for fila in lector:
            materia = fila["Materia"]
            if materia in wanted_classes:
                seccion_id = int(fila["Sección"])
                dia = fila["Día"]
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


def superposicion(a: Seccion, b: Seccion) -> bool:
    """
    TRUE si los horarios de a y b se superponen
    FALSE caso contrario
    """
    horarios_a= a.horarios #lista de tuplas
    horarios_b= b.horarios
    for clase in horarios_a:
        if clase in horarios_b:
            return True
    return False

#Ahora armo las combinaciones que no se superpongan. Fuerza bruta + backtraking? 
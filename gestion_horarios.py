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


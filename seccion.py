### defincin de clase Seccion

class Seccion: 
    def __init__(self, materia, seccion_id, horarios):
        self.materia = materia #str
        self.seccion_id = seccion_id #int
        self.horarios = horarios  # Lista de tuplas (dia, timeslot, tipo). una tupla x clase

    def __repr__(self):
        return f"{self.materia} Sección{self.seccion_id}: {self.horarios}"

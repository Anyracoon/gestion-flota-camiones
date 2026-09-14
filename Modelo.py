class EmpresaCamiones:
    def __init__(self):
        # Aquí se guardará la lista de todos los vehículos registrados
        self.registro_vehiculos = []

    def guardar_vehiculo(self, datos_vehiculo):
        self.registro_vehiculos.append(datos_vehiculo)
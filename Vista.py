class VistaConsola:
    def __init__(self):
        self.separador = "=" * 55

    def mostrar_menu_principal(self):
        print(f"\n{self.separador}")
        print("     SISTEMA DE GESTIÓN DE FLOTA DE CAMIONES     ")
        print(self.separador)
        print("1. Registrar vehículos")
        print("2. Visualizar registros")
        print("3. Salir")
        print(self.separador)
        return input("Por favor, seleccione una opción (ej. 1, registrar, salir): ")

    def preguntar_tipo_registro(self):
        print(f"\n{self.separador}")
        print("            OPCIONES DE REGISTRO            ")
        print(self.separador)
        print("1. Registrar una cantidad definida (N) de vehículos")
        print("2. Registrar una cantidad indefinida")
        return input("Indique su preferencia (ej. 1, 2, n, indefinida): ")

    def pedir_cantidad_n(self):
        return input("\nPor favor, indique cuántos vehículos desea registrar: ")

    def solicitar_datos_vehiculo(self):
        print(f"\n--- Ingrese los datos del vehículo ---")
        camion = input("Identificación/Placa del camión: ")
        conductor = input("Nombre del conductor: ")
        hora_salida = input("Hora de salida (ej. 08:00): ")
        km = input("Kilómetros recorridos: ")
        hora_llegada = input("Hora de llegada (ej. 18:00): ")
        lote = input("Lote al que pertenece el vehículo: ")
        
        return {
            "camion": camion,
            "conductor": conductor,
            "hora_salida": hora_salida,
            "kilometros": km,
            "hora_llegada": hora_llegada,
            "lote": lote
        }

    def preguntar_continuar(self):
        return input("\n¿Desea continuar ingresando valores? (si/no): ")

    def preguntar_accion_final(self):
        print(f"\n{self.separador}")
        print("¿Qué desea hacer a continuación?")
        print("1. Realizar otra acción (Volver al menú principal)")
        print("2. Salir del programa")
        return input("Seleccione su opción (1/2, volver, salir): ")

    def mensaje_error(self, mensaje):
        print(f"\n[!] Atención: {mensaje}")

    def despedida(self):
        print("\nGracias por utilizar el sistema de la empresa de camiones. ¡Hasta pronto!")
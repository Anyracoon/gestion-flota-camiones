class VistaConsola:
    def __init__(self):
        # Separador para darle estilo y estructura al menú por consola
        self.separador = "=" * 85

    def mostrar_menu_principal(self):
        print(f"\n{self.separador}")
        print("                 SISTEMA DE GESTIÓN DE FLOTA DE CAMIONES                 ")
        print(self.separador)
        print("1. Registrar vehículos")
        print("2. Visualizar registros (Búsqueda avanzada)")
        print("3. Salir")
        print(self.separador)
        return input("Por favor, seleccione una opción (ej. 1, 2, 3): ")

    def preguntar_tipo_registro(self):
        print(f"\n{self.separador}")
        print("                          OPCIONES DE REGISTRO                           ")
        print(self.separador)
        print("1. Registrar una cantidad definida (N) de vehículos")
        print("2. Registrar una cantidad indefinida")
        return input("Indique su preferencia: ")

    def pedir_cantidad_n(self):
        return input("\nPor favor, indique cuántos vehículos desea registrar: ")

    def pedir_dato_vehiculo(self, mensaje):
        """
        Método genérico para solicitar un dato individual.
        Delega la validación al controlador.
        """
        return input(f"{mensaje}: ")

    def preguntar_continuar(self):
        return input("\n¿Desea continuar ingresando valores? (si/no): ")

    def preguntar_accion_final(self):
        print(f"\n{self.separador}")
        print("¿Qué desea hacer a continuación?")
        print("1. Realizar otra acción (Volver al menú principal)")
        print("2. Salir del programa")
        return input("Seleccione su opción (1/2): ")

    def mensaje_error(self, mensaje):
        print(f"\n[!] Atención: {mensaje}")

    def despedida(self):
        print("\nGracias por utilizar el sistema de la empresa de camiones. ¡Hasta pronto!")

    def mostrar_menu_busqueda(self):
        print(f"\n{self.separador}")
        print("                          CRITERIOS DE BÚSQUEDA                          ")
        print(self.separador)
        print("1. Por placa del vehículo")
        print("2. Por nombre del conductor")
        print("3. Por lote al que pertenece")
        print("4. Por rango de kilómetros recorridos")
        print("5. Por lapso de tiempo (Hora de salida)")
        print("6. Volver al menú principal")
        print(self.separador)
        return input("Seleccione el criterio de búsqueda (1-6): ")

    def mostrar_tabla_vehiculos(self, vehiculos):
        """
        Recibe una lista de diccionarios y los renderiza en un formato de tabla
        alineada por consola para su fácil lectura.
        """
        if not vehiculos:
            print("\n[!] No se encontraron registros con los criterios especificados.")
            return

        print("\n" + self.separador)
        # Formateo de columnas con anchos fijos para mantener la simetría
        print(f"{'PLACA':<10} | {'CONDUCTOR':<20} | {'SALIDA':<8} | {'LLEGADA':<8} | {'KM':<8} | {'LOTE':<12}")
        print("-" * 85)
        
        for v in vehiculos:
            # Los textos se muestran en formato título o mayúscula para mejor presentación
            print(f"{v['camion']:<10} | {v['conductor'].title():<20} | {v['hora_salida']:<8} | {v['hora_llegada']:<8} | {v['kilometros']:<8.1f} | {v['lote'].title():<12}")
        
        print(self.separador)
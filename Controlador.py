import re
from datetime import datetime
import sys

class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def a_minusculas(self, texto):
        """Pasa a minúsculas y quita espacios en los bordes."""
        return str(texto).strip().lower()

    # ==========================================
    # FUNCIONES DE VALIDACIÓN (El filtro estricto)
    # ==========================================

    def validar_placa(self, placa_cruda):
        """Valida que la placa tenga 3 letras y 3 números y la pasa a mayúsculas."""
        placa_limpia = str(placa_cruda).replace(" ", "")
        patron_1 = r'^[A-Za-z]{3}\d{3}$'
        patron_2 = r'^\d{3}[A-Za-z]{3}$'
        
        if re.match(patron_1, placa_limpia) or re.match(patron_2, placa_limpia):
            return placa_limpia.upper()
        return None

    def validar_hora(self, hora_cruda):
        """Valida que la hora sea real y esté en formato HH:MM."""
        try:
            hora_valida = datetime.strptime(str(hora_cruda).strip(), "%H:%M")
            return hora_valida.strftime("%H:%M")
        except ValueError:
            return None

    def validar_km(self, km_crudo):
        """Valida que los km sean numéricos y positivos."""
        try:
            km = float(km_crudo)
            if km < 0:
                return None
            return km
        except ValueError:
            return None

    # ==========================================
    # RECOPILACIÓN Y GUARDADO DE DATOS
    # ==========================================

    def solicitar_y_validar_datos(self):
        """Encierra al usuario hasta que meta todos los datos como se debe."""
        print("\n--- Ingrese los datos del vehículo ---")
        
        while True:
            placa = self.vista.pedir_dato_vehiculo("Placa del camión (3 letras y 3 números)")
            placa_valida = self.validar_placa(placa)
            if placa_valida:
                break
            self.vista.mensaje_error("Placa inválida. Recuerde: 3 letras y 3 números, sin importar el orden.")

        conductor_crudo = self.vista.pedir_dato_vehiculo("Nombre del conductor")
        conductor = self.a_minusculas(conductor_crudo)

        while True:
            h_salida = self.vista.pedir_dato_vehiculo("Hora de salida (HH:MM)")
            h_salida_valida = self.validar_hora(h_salida)
            if h_salida_valida:
                break
            self.vista.mensaje_error("Hora inválida. Use el formato de 24 horas (ej. 08:30).")

        while True:
            km = self.vista.pedir_dato_vehiculo("Kilómetros recorridos")
            km_valido = self.validar_km(km)
            if km_valido is not None:
                break
            self.vista.mensaje_error("Kilómetros inválidos. Ingrese un número positivo.")

        while True:
            h_llegada = self.vista.pedir_dato_vehiculo("Hora de llegada (HH:MM)")
            h_llegada_valida = self.validar_hora(h_llegada)
            if h_llegada_valida:
                break
            self.vista.mensaje_error("Hora inválida. Use formato HH:MM.")

        lote_crudo = self.vista.pedir_dato_vehiculo("Lote al que pertenece")
        lote = self.a_minusculas(lote_crudo)

        return {
            "camion": placa_valida,
            "conductor": conductor,
            "hora_salida": h_salida_valida,
            "kilometros": km_valido,
            "hora_llegada": h_llegada_valida,
            "lote": lote
        }

    def guardar_vehiculo_seguro(self, datos):
        """Delega el guardado al modelo y maneja el error si el Excel está abierto."""
        exito = self.modelo.guardar_vehiculo(datos)
        if not exito:
            self.vista.mensaje_error("No se pudo guardar. ¡Cierre el archivo CSV en Excel e intente de nuevo, baka!")

    # ==========================================
    # FLUJOS PRINCIPALES
    # ==========================================

    def flujo_registro(self):
        """Maneja el registro de N vehículos o indefinidos."""
        tipo = self.a_minusculas(self.vista.preguntar_tipo_registro())

        if tipo in ['1', 'n', 'definida']:
            try:
                n_str = self.a_minusculas(self.vista.pedir_cantidad_n())
                n = int(n_str)
                for _ in range(n):
                    datos_limpios = self.solicitar_y_validar_datos()
                    self.guardar_vehiculo_seguro(datos_limpios)
            except ValueError:
                self.vista.mensaje_error("Debe ingresar un número válido para la cantidad.")

        elif tipo in ['2', 'indefinida']:
            while True:
                datos_limpios = self.solicitar_y_validar_datos()
                self.guardar_vehiculo_seguro(datos_limpios)

                continuar = self.a_minusculas(self.vista.preguntar_continuar())
                if continuar == 'no':
                    break
        else:
            self.vista.mensaje_error("Opción de registro no reconocida.")
            return

        self.manejar_salida()

    def manejar_salida(self):
        """Submenú después de registrar para volver o matar el programa."""
        accion = self.a_minusculas(self.vista.preguntar_accion_final())
        if accion in ['2', 'salir']:
            self.vista.despedida()
            sys.exit()

    # ==========================================
    # FLUJOS DE BÚSQUEDA
    # ==========================================

    def obtener_registros_seguro(self):
        """Solicita los datos al modelo y revisa que no haya error de permisos."""
        registros = self.modelo.obtener_todos()
        if registros is None:
            self.vista.mensaje_error("El archivo CSV está bloqueado. Ciérrelo en otro programa para poder buscar.")
            return []
        return registros

    def flujo_busqueda(self):
        """Menú que despacha los diferentes tipos de filtros sobre el CSV."""
        while True:
            opcion = self.a_minusculas(self.vista.mostrar_menu_busqueda())
            todos = self.obtener_registros_seguro()
            
            # Si la lista de todos viene vacía y la opción no es salir, vuelve a preguntar
            if not todos and opcion not in ['6', 'volver']:
                continue

            if opcion in ['1', 'placa']:
                placa = self.vista.pedir_dato_vehiculo("Ingrese la placa a buscar")
                placa_limpia = placa.replace(" ", "").upper()
                filtrados = [v for v in todos if v["camion"] == placa_limpia]
                self.vista.mostrar_tabla_vehiculos(filtrados)

            elif opcion in ['2', 'conductor']:
                busqueda = self.a_minusculas(self.vista.pedir_dato_vehiculo("Ingrese el nombre del conductor"))
                filtrados = [v for v in todos if busqueda in v["conductor"]]
                self.vista.mostrar_tabla_vehiculos(filtrados)

            elif opcion in ['3', 'lote']:
                lote = self.a_minusculas(self.vista.pedir_dato_vehiculo("Ingrese el lote"))
                filtrados = [v for v in todos if v["lote"] == lote]
                self.vista.mostrar_tabla_vehiculos(filtrados)

            elif opcion in ['4', 'kilometros', 'km']:
                self._buscar_por_rango_km(todos)

            elif opcion in ['5', 'tiempo', 'hora']:
                self._buscar_por_lapso_tiempo(todos)

            elif opcion in ['6', 'volver']:
                break
            else:
                self.vista.mensaje_error("Opción de búsqueda no válida.")

    def _buscar_por_rango_km(self, registros):
        """Filtra camiones dentro de un intervalo cerrado [min_km, max_km]."""
        while True:
            min_km_str = self.vista.pedir_dato_vehiculo("Kilometraje mínimo")
            max_km_str = self.vista.pedir_dato_vehiculo("Kilometraje máximo")
            
            min_km = self.validar_km(min_km_str)
            max_km = self.validar_km(max_km_str)

            if min_km is not None and max_km is not None:
                if min_km <= max_km:
                    filtrados = [v for v in registros if min_km <= v["kilometros"] <= max_km]
                    self.vista.mostrar_tabla_vehiculos(filtrados)
                    break
                else:
                    self.vista.mensaje_error("El km mínimo no puede ser mayor que el máximo, baka.")
            else:
                self.vista.mensaje_error("Ingrese valores numéricos positivos para los kilómetros.")

    def _buscar_por_lapso_tiempo(self, registros):
        """Filtra registros cuya hora de salida caiga dentro del rango especificado."""
        while True:
            h_inicio_str = self.vista.pedir_dato_vehiculo("Hora inicio del lapso (HH:MM)")
            h_fin_str = self.vista.pedir_dato_vehiculo("Hora fin del lapso (HH:MM)")

            if self.validar_hora(h_inicio_str) and self.validar_hora(h_fin_str):
                t_inicio = datetime.strptime(h_inicio_str.strip(), "%H:%M").time()
                t_fin = datetime.strptime(h_fin_str.strip(), "%H:%M").time()

                if t_inicio <= t_fin:
                    filtrados = []
                    for v in registros:
                        t_salida = datetime.strptime(v["hora_salida"], "%H:%M").time()
                        if t_inicio <= t_salida <= t_fin:
                            filtrados.append(v)
                    self.vista.mostrar_tabla_vehiculos(filtrados)
                    break
                else:
                    self.vista.mensaje_error("La hora inicial debe ser menor o igual a la hora final.")
            else:
                self.vista.mensaje_error("Formato de hora incorrecto. Use HH:MM en formato 24 horas.")

    # ==========================================
    # PUNTO DE ARRANQUE DEL CONTROLADOR
    # ==========================================

    def iniciar(self):
        """El ciclo de vida principal que mantiene vivo el menú."""
        while True:
            opcion = self.a_minusculas(self.vista.mostrar_menu_principal())

            if opcion in ['1', 'registrar']:
                self.flujo_registro()
            elif opcion in ['2', 'visualizar']:
                self.flujo_busqueda()
            elif opcion in ['3', 'salir']:
                self.vista.despedida()
                break
            else:
                self.vista.mensaje_error("Opción no válida. Intente nuevamente.")
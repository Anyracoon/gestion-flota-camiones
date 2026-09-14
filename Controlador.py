import re
from datetime import datetime
import sys

class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def a_minusculas(self, texto):
        """Pasa a minúsculas y quita espacios en blanco de los bordes."""
        return str(texto).strip().lower()

    # ==========================================
    # FUNCIONES DE VALIDACIÓN (El celador estricto)
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

    def solicitar_y_validar_datos(self):
        """Encierra al usuario hasta que meta los datos como se debe."""
        print("\n--- Ingrese los datos del vehículo ---")
        
        # 1. Placa
        while True:
            placa = self.vista.pedir_dato_vehiculo("Placa del camión (3 letras y 3 números)")
            placa_valida = self.validar_placa(placa)
            if placa_valida:
                break
            self.vista.mensaje_error("Placa inválida. Recuerde: 3 letras y 3 números sin importar el orden.")

        # 2. Conductor
        conductor_crudo = self.vista.pedir_dato_vehiculo("Nombre del conductor")
        conductor = self.a_minusculas(conductor_crudo)

        # 3. Hora de salida
        while True:
            h_salida = self.vista.pedir_dato_vehiculo("Hora de salida (HH:MM)")
            h_salida_valida = self.validar_hora(h_salida)
            if h_salida_valida:
                break
            self.vista.mensaje_error("Hora inválida. Use el formato de 24 horas (ej. 08:30).")

        # 4. Kilómetros
        while True:
            km = self.vista.pedir_dato_vehiculo("Kilómetros recorridos")
            km_valido = self.validar_km(km)
            if km_valido is not None:
                break
            self.vista.mensaje_error("Kilómetros inválidos. Ingrese un número positivo.")

        # 5. Hora de llegada
        while True:
            h_llegada = self.vista.pedir_dato_vehiculo("Hora de llegada (HH:MM)")
            h_llegada_valida = self.validar_hora(h_llegada)
            if h_llegada_valida:
                break
            self.vista.mensaje_error("Hora inválida. Use formato HH:MM.")

        # 6. Lote
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

    # ==========================================
    # FLUJOS DEL PROGRAMA
    # ==========================================

    def flujo_registro(self):
        """Maneja si se ingresan N vehículos o de forma indefinida."""
        tipo = self.a_minusculas(self.vista.preguntar_tipo_registro())

        if tipo in ['1', 'n', 'definida']:
            try:
                n_str = self.a_minusculas(self.vista.pedir_cantidad_n())
                n = int(n_str)
                for _ in range(n):
                    datos_limpios = self.solicitar_y_validar_datos()
                    self.modelo.guardar_vehiculo(datos_limpios)
            except ValueError:
                self.vista.mensaje_error("Debe ingresar un número válido para la cantidad.")

        elif tipo in ['2', 'indefinida']:
            while True:
                datos_limpios = self.solicitar_y_validar_datos()
                self.modelo.guardar_vehiculo(datos_limpios)

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

    def iniciar(self):
        """Punto de entrada, el ciclo principal de vida del programa."""
        while True:
            opcion = self.a_minusculas(self.vista.mostrar_menu_principal())

            if opcion in ['1', 'registrar']:
                self.flujo_registro()
            elif opcion in ['2', 'visualizar']:
                print("\n[Módulo de visualización en construcción... ¡no me acose, baka!]")
            elif opcion in ['3', 'salir']:
                self.vista.despedida()
                break
            else:
                self.vista.mensaje_error("Opción no válida. Intente nuevamente.")
import re
from datetime import datetime

class Controlador:
    def __init__(self, modelo, vista):
        self.modelo = modelo
        self.vista = vista

    def a_minusculas(self, texto):
        return str(texto).strip().lower()

    # --- NUEVAS FUNCIONES DE VALIDACIÓN ---

    def validar_placa(self, placa_cruda):
        """Quita espacios, valida 3 letras y 3 números (o viceversa) y la pone en mayúscula."""
        # Quitamos espacios en blanco
        placa_limpia = placa_cruda.replace(" ", "")
        
        # Regex: ^ = inicio, $ = fin. Buscamos 3 letras y 3 números en cualquier orden común
        # (ej: ABC123 o 123ABC)
        patron_1 = r'^[A-Za-z]{3}\d{3}$'
        patron_2 = r'^\d{3}[A-Za-z]{3}$'
        
        if re.match(patron_1, placa_limpia) or re.match(patron_2, placa_limpia):
            return placa_limpia.upper() # La excepción a su regla de minúsculas
        else:
            return None # Retorna None si el baka del usuario metió mal la placa

    def validar_hora(self, hora_cruda):
        """Valida que la hora tenga formato HH:MM y sea lógica."""
        try:
            # Intenta convertir el string a un objeto de tiempo
            hora_valida = datetime.strptime(hora_cruda.strip(), "%H:%M")
            # Si funciona, lo devuelve formateado bonito como string para el CSV
            return hora_valida.strftime("%H:%M")
        except ValueError:
            return None # Si mete "hola" o "-05:00", paila

    def validar_km(self, km_crudo):
        """Valida que sean números y que no sean negativos."""
        try:
            km = float(km_crudo)
            if km < 0:
                return None
            return km
        except ValueError:
            return None
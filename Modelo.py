import csv
import os

class EmpresaCamiones:
    def __init__(self, ruta_archivo="registro_camiones.csv"):
        self.archivo_csv = ruta_archivo
        self.campos = [
            "camion", 
            "conductor", 
            "hora_salida", 
            "kilometros", 
            "hora_llegada", 
            "lote"
        ]
        self._inicializar_archivo()

    def _inicializar_archivo(self):
        """Crea el archivo con encabezados si no existe o si está vacío (0 bytes)."""
        necesita_encabezado = not os.path.exists(self.archivo_csv) or os.path.getsize(self.archivo_csv) == 0
        
        if necesita_encabezado:
            try:
                with open(self.archivo_csv, mode='w', newline='', encoding='utf-8') as archivo:
                    escritor = csv.DictWriter(archivo, fieldnames=self.campos)
                    escritor.writeheader()
            except PermissionError:
                raise PermissionError(f"No se pudo inicializar '{self.archivo_csv}'. El archivo está bloqueado por otro programa.")

    def guardar_vehiculo(self, datos_vehiculo):
        """Guarda un registro nuevo en el CSV manejando bloqueos de archivo."""
        try:
            with open(self.archivo_csv, mode='a', newline='', encoding='utf-8') as archivo:
                escritor = csv.DictWriter(archivo, fieldnames=self.campos)
                escritor.writerow(datos_vehiculo)
            return True
        except PermissionError:
            return False

    def obtener_todos(self):
        """Lee y entrega todos los registros convirtiendo campos numéricos."""
        if not os.path.exists(self.archivo_csv) or os.path.getsize(self.archivo_csv) == 0:
            return []

        registros = []
        try:
            with open(self.archivo_csv, mode='r', newline='', encoding='utf-8') as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    # Garantizamos el tipo de dato para el controlador
                    try:
                        fila["kilometros"] = float(fila.get("kilometros", 0.0))
                    except (ValueError, TypeError):
                        fila["kilometros"] = 0.0
                    registros.append(fila)
        except PermissionError:
            return None # Señal de que el archivo está abierto en otra app
        
        return registros

    def existe_camion(self, placa):
        """Verifica de forma rápida si una placa ya cuenta con historial en el sistema."""
        registros = self.obtener_todos()
        if not registros:
            return False
        return any(v["camion"] == placa.upper() for v in registros)
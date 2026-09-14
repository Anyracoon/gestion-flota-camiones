# main.py

# Importación de los módulos correspondientes a la arquitectura MVC
from Modelo import EmpresaCamiones
from Vista import VistaConsola
from Controlador import Controlador

if __name__ == "__main__":
    # Inicialización de las capas de Modelo y Vista
    modelo_app = EmpresaCamiones()
    vista_app = VistaConsola()
    
    # Inyección de dependencias en el Controlador para orquestar la aplicación
    controlador_app = Controlador(modelo_app, vista_app)
    
    # Ejecución del ciclo de vida principal del programa
    controlador_app.iniciar()
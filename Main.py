# main.py

# Importamos las clases desde los otros archivos de la vuelta
from modelo import EmpresaCamiones
from vista import VistaConsola
from controlador import Controlador

if __name__ == "__main__":
    # Instanciamos los objetos, pille cómo se conectan
    modelo_app = EmpresaCamiones()
    vista_app = VistaConsola()
    
    # El controlador es el celador y necesita conocer a los otros dos
    controlador_app = Controlador(modelo_app, vista_app)
    
    # Arrancamos el ciclo
    controlador_app.iniciar()
"""
Configuración global del servidor: host, puerto, y constantes relacionadas con la red y base de datos.
"""
from pathlib import Path  # Añade esta línea en la parte superior
import os



HOST = "localhost"
PORT = 5000
# Ruta absoluta
DB_NAME = str(Path(__file__).parent.parent.parent / "data" / "mensajes.db")
BUFFER_SIZE = 1024
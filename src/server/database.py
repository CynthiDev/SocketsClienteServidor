"""
Módulo de base de datos: maneja la creación de tablas y operaciones de almacenamiento.
"""

import sqlite3
from datetime import datetime
from ..server.config import DB_NAME

class DatabaseManager:


    def __init__(self):
        """Inicializa la conexión a la base de datos y crea la tabla si no existe."""
        # Cada hilo tendrá su propia conexión
        self.conn = sqlite3.connect(DB_NAME, check_same_thread=False)  # Permite uso en múltiples hilos
        self._create_table()



    def _create_table(self):
        """Crea la tabla 'mensajes' si no está creada en la base de datos."""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT,
                fecha_envio DATETIME,
                ip_cliente TEXT
            )
        ''')
        self.conn.commit()


    def save_message(self, content, client_ip):
        """
        Guarda un mensaje en la base de datos.
        Args:
            content (str): Contenido del mensaje.
            client_ip (str): Dirección IP del cliente.
        Returns:
            bool: True si el mensaje se guardó correctamente, False en caso de error.
        """
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
                VALUES (?, ?, ?)
            ''', (content, datetime.now(), client_ip))
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Database error: {e}")
            return False

    def close(self):
        self.conn.close()
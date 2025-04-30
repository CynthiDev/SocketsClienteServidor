"""
Cliente: permite conectarse al servidor y enviar mensajes interactivamente.
"""

import socket
from ..shared.utils import get_timestamp
from ..server.config import HOST, PORT, BUFFER_SIZE

class ChatClient:
    """ Cliente para interactuar con el servidor de chat. """


    def __init__(self):
        """Inicializa el socket del cliente."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    


    def conectar_con_servidor(self):
        """
        Establece conexión con el servidor y maneja el envío/recepción de mensajes.
        """
        try:
            self.client_socket.connect((HOST, PORT))
            print(f"Conectado a  {HOST}:{PORT}. Escribe 'éxito' para salir.")
            self._enviar_mensajes()
        except ConnectionRefusedError:
            print("Error: El servidor no está disponible o no está corriendo.")
        except Exception as e:
            print(f"Conneccion error: {e}")
        finally:
            self.client_socket.close()



    def _enviar_mensajes(self):
        """Recibe input del usuario y envía mensajes al servidor hasta que se ingrese 'éxito'."""
        try:
            while True:
                message = input(">> ")
                self.client_socket.send(message.encode('utf-8'))
                
                if message.lower().strip() == 'éxito':
                    print("Desconectando del servidor...")
                    break
                
                # Esperar respuesta del servidor
                try:
                    response = self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
                    print(f"Servidor: {response}")
                except (ConnectionResetError, BrokenPipeError):
                    print("Error: El servidor cerró la conexión")
                    break
        except KeyboardInterrupt:
            print("\nCliente detenido manualmente")



if __name__ == "__main__":
    client = ChatClient()
    client.conectar_con_servidor()
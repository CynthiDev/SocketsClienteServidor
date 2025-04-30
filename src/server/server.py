import socket
import threading
from .config import HOST, PORT, BUFFER_SIZE
from .database import DatabaseManager
from ..shared.utils import get_timestamp  


class ChatServer:
    """Servidor principal que gestiona conexiones de clientes y mensajes."""


    def __init__(self):
        """Inicializa el socket del servidor y el administrador de la base de datos."""
        self.servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.db = DatabaseManager()

   
    def iniciar_servidor(self):
        """
        Inicia el servidor, vinculando el socket al host:puerto y escuchando conexiones.
        Acepta clientes en hilos separados.
        """
        try:
            self.servidor_socket.bind((HOST, PORT))
            self.servidor_socket.listen(5)
            print(f"Servidor escuchando en: {HOST}:{PORT}")
            
            while True:
                cliente, direccion = self.servidor_socket.accept()
                print(f"Nueva conexión: {direccion}")
                hiloCliente = threading.Thread(
                    target=self.gestionar_cliente,
                    args=(cliente, direccion)
                )
                hiloCliente.start()
                
        except Exception as e:
            print(f"Servidor error: {e}")
        finally:
            self.servidor_socket.close()



    def gestionar_cliente(self, client_socket, direccion: tuple):
        """
        Maneja la comunicación con un cliente conectado.
        Args:
            client_socket (socket.socket): Socket del cliente.
            addr (tuple): Tupla con la dirección IP y puerto del cliente.
        """
        baseDeDatos = DatabaseManager()    # Conexión independiente por CADA hilo/cliente
        try:
            while True:
                try:
                    message = client_socket.recv(BUFFER_SIZE).decode('utf-8')
                    if not message or message.lower().strip() == 'éxito':
                        break  # Salir si el mensaje es vacío o "éxito"

                    if message.lower().strip() == 'éxito':
                        print(f"Cliente {direccion} cerró la conexión correctamente.")
                        break
                    

                    # Guardar mensaje y responder
                    if baseDeDatos.save_message(message, direccion[0]):
                        response = f"Mensaje recibido: {get_timestamp()}"
                    else:
                        response = "Error al guardar mensaje"
                    
                    client_socket.send(response.encode('utf-8'))

                except (ConnectionResetError, BrokenPipeError):
                    print(f"Cliente {direccion} desconectado abruptamente")
                    break
        
        except Exception as e:
            print(f"Client error ({direccion}): {e}")
        finally:
            baseDeDatos.close()  # Cierra la conexión al finalizar el hilo
            client_socket.close()
            print(f"Conexión con {direccion} finalizada.")










if __name__ == "__main__":
    server = ChatServer()
    server.iniciar_servidor()
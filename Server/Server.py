# Importar librerias para el manejo del sistema, algoritmos de hash, tiempos, captura de paquetes, manejo de threads, manejo de sockets y funciones definidas en el archivo utils
from Utils import *
import socket
import os
import threading
import time
from datetime import datetime
#import pyshark

# Constantes SEPARATOR, BUFFER_SIZE y BUFFER_SIZE_UDP
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
BUFFER_SIZE_UDP = 30000

# Creacion del socket tcp lado del servidor
ServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 9879
portUDP = 12000
try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

# Ingresar el numero de clientes a conectar al servicio
NUM_CLIENTES = int(input("Ingrese el numero de clientes a conectar: "))

# Imprimir en la consola los archivos disponibles para hacer el envio a los clientes
print_files()

# Seleccionar el archivo que quiere enviar a los clientes
numberFile = input("Escoge el archivo a enviar (1 o 2): ")
FILE_NAME = None
n = False
FILE_NAME = get_file(numberFile)

print('Esperando las conexiones de los clientes...')
ServerSocket.listen(5)

# Contador del numero de threads ejecutandose
contador = 0

# Tamanio del archivo correspondiente a enviar
FILE_SIZE = os.path.getsize(FILE_NAME)

# Funcion que correr cada thread la cual consiste en el envio del archivo, el hash y la recepcion de confirmacion de integridad
# Por cada thread que se corre se genera un archivo log que contiene la informacion respectiva detalla segun las especificaciones de la guia
def threaded_client(connection, connectionUDP, serverAdr):

    # Tiempo de incio de ejecucion
    start_time = datetime.now()

    global contador 
    # Envio del archivo ocurre cuando todos los clientes esten listos
    with connection as c:
        data = c.recv(BUFFER_SIZE)
            
        if data.decode('utf-8')=="listo":
            contador+=1
            numero = contador 
            while contador < NUM_CLIENTES:   
                continue 
            extension = FILE_NAME.split('.')[2]
            c.send(f"Cliente{numero}-Prueba-{NUM_CLIENTES}.{extension}{SEPARATOR}{FILE_SIZE}".encode())

            mensaje, address = connectionUDP.recvfrom(BUFFER_SIZE_UDP)
            with open(FILE_NAME, "rb") as f:
                while True:
                    # leer los bytes del archivo
                    bytes_read = f.read(BUFFER_SIZE_UDP)

                    if not bytes_read:
                        break

                    # Enviar el paquete por el socket UDP
                    connectionUDP.sendto(bytes_read, address)

    # Cerrar la conexion del socket     
    connectionUDP.close()
    
    # Tiempo final de ejecucion
    finish_time = datetime.now()

    # Escritura del archivo log con la informacion establecida en la guia
    write_log_file(FILE_NAME, FILE_SIZE, numero, "No se entrega el archivo exitosamente", start_time, finish_time)

# Contador del numero de threads local para el while
ThreadCount = 0

# Creacion de threads, entablar conexiones y iniciar el metodo threade_client de cada thread
while ThreadCount < NUM_CLIENTES:
    Client, address = ServerSocket.accept()
    print("Conectado con: " + address[0] + ":" + str(address[1]))

    # Creacion del socket UDP
    ServerSockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (host, portUDP)
    ServerSockUDP.bind(server_address)

    # Creacion de los threads
    threading.Thread(target=threaded_client, args=(Client, ServerSockUDP, server_address, )).start()
    
    # Cambiar de puerto para el otro socket UDP
    portUDP = portUDP + 1
    ThreadCount += 1
    print("Numero del Thread: " + str(ThreadCount))

# Cerrar la conexion del socket
ServerSocket.close()
# Importar librerias para el manejo del sistema, algoritmos de hash, tiempos, captura de paquetes, manejo de threads, manejo de sockets y funciones definidas en el archivo utils
import socket
import os
import threading
from Utils import write_log_file
import time
from datetime import datetime
import pyshark

# Constantes SEPARATOR, BUFFER_SIZE, HOST y PORT
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
BUFFER_SIZE_UDP = 30000
HOST = '127.0.0.1'
PORT = 9879
PORT_UDP = 12000

# Contador del numero de threads ejecutandose
contador = 0

# Funcion que correr cada thread la cual consiste en recibir el archivo, el hash y la recepcion de confirmacion de integridad
# Por cada thread que se corre se genera un archivo log que contiene la informacion respectiva detalla segun las especificaciones de la guia
def correr_clientes(ClientSocket, ClientSocketUDP, ServerAddress):

    # Contador global del numero de threads
    global contador 
    contador+=1

    # Captura de paquetes por la interfaz de ethernet 
    capture = pyshark.LiveCapture(interface='Ethernet')
    capture.sniff(timeout=1)

    # Tiempo de incio de ejecucion
    start_time = datetime.now()

    # Entablar conexiones con el el servidor para empezar la transferencia del archivo
    try:
        ClientSocket.connect((HOST, PORT))
        mensaje = "listo"
        ClientSocket.send(str.encode(mensaje))
        received = ClientSocket.recv(BUFFER_SIZE).decode()

        # Variables correspondientes al nombre del archivo y tamanio del archivo
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        sent = ClientSocketUDP.sendto(b"Empezar", ServerAddress)

        # Escritura del archivo recibido por partes desde el servidor
        with open('./ArchivosRecibidos/'+ filename, "wb") as f:
            while True:
                #print("2.1")
                bytes_read, address = ClientSocketUDP.recvfrom(BUFFER_SIZE_UDP)
                ClientSocketUDP.settimeout(60)
                f.write(bytes_read)

    except socket.error as e:
        print("Vamos bien")
        # Tiempo final de ejecucion
        finish_time = datetime.now()

        # Escritura del archivo log con la informacion establecida en la guia
        numeropack=str(capture).replace("<LiveCapture (","").replace(" packets)>","")
        write_log_file(filename, filesize, contador, "No se entrega el archivo exitosamente", start_time, finish_time, int(numeropack))

        print("Un thread ha acabado:" + str(e))
        # Cerrar la conexion del socket
        ClientSocketUDP.close()
        ClientSocket.close()
    
# Ingresar el numero de clientes a establecer conexion
numClientes = int(input("Ingrese el número de clientes: "))

# Contador del numero de threads local para el while
ThreadCount = 0

# Creacion de sockets asociados a los threads y iniciar el metodo correr_cliente de cada thread
while ThreadCount < numClientes:
    # Creacion del socket TCP
    Client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Creacion del socket UDP
    ClientUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (HOST, PORT_UDP)

    # Creacion de los threads
    threading.Thread(target=correr_clientes, args=(Client, ClientUDP, server_address, )).start()

    # Cambiar de puerto para el otro socket UDP
    PORT_UDP = PORT_UDP + 1
    time.sleep(1)
    ThreadCount += 1
    print("Numero del Thread: " + str(ThreadCount))
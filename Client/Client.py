import socket
import os
import threading
from Utils import write_log_file
import time
from datetime import datetime


# Constantes SEPARATOR, BUFFER_SIZE, HOST y PORT
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
BUFFER_SIZE_UDP = 30000
HOST = '192.168.152.131'
PORT = 9879
PORT_UDP = 12000


contador = 0

def correr_clientes(ClientSocket, ClientSocketUDP, ServerAddress):
    global contador 
    contador+=1

    start_time = datetime.now()


    try:
        ClientSocket.connect((HOST, PORT))
        mensaje = "listo"
        ClientSocket.send(str.encode(mensaje))
        received = ClientSocket.recv(BUFFER_SIZE).decode()

        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filesize = int(filesize)

        sent = ClientSocketUDP.sendto(b"Empezar", ServerAddress)

        with open( "./Client/ArchivosRecibidos/"+filename, "wb") as f:
            while True:
                #print("2.1")
                bytes_read, address = ClientSocketUDP.recvfrom(BUFFER_SIZE_UDP)
                ClientSocketUDP.settimeout(60)
                f.write(bytes_read)

        

    except socket.error as e:
        print("Vamos bien")
        finish_time = datetime.now()
        tiempo = finish_time - start_time
        #write_log_file(filename, filesize, "No se entrega el archivo exitosamente", tiempo, contador )

        print("Un thread ha acabado:" + str(e))
        # Cerrar la conexion del socket
        ClientSocketUDP.close()
        ClientSocket.close()

        
    finish_time = datetime.now()
    tiempo = finish_time - start_time
    write_log_file(filename, filesize, "Se entrega exitosamente", tiempo, contador )
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
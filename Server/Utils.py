# Importar librerias para el manejo del sistema, tiempos y captura de paquetes
import os
import datetime

# Funcion para imprimir los archivos diponibles en el servidor (prueba100MB y prueba250 MB)
def print_files():
    files_server = os.listdir('./files/')
    print("Los archivos que estan disponibles en el servidor son:")
    for i in range (len(files_server)):
        print(str(i+1) + "." + files_server[i])

# Funcion para obtener el archivo dado el numero ingresado como parametro
def get_file (num_file):
    archivo = ''
    if num_file == "1":
        archivo = './files/prueba100MB.txt'
    elif num_file == "2":
        archivo = './files/prueba250MB.txt'
    return archivo

# Funcion para generar el archivo de log en el directorio llamado Logs con la informacion determinada en la guia
def write_log_file (file_name, file_size, num_client, status_file, start_time, finish_time):
    today = datetime.datetime.now()
    name_file = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "-" + str(today.hour) + "-" + str(today.minute) + "-" + str(today.second) + "-" + str(today.microsecond) + str(num_client) + "-log.txt"
    log_file = open("./Logs/" + name_file, "w")
    log_file.write("Nombre del archivo: " + file_name.split("/")[2] + "\n")
    log_file.write("Tamanio del archivo: " + str(file_size) + "\n")
    log_file.write("Cliente al que se realiza la transeferencia de archivos: " + str(num_client) + "\n")
    log_file.write("Estado de entrega del archivo: " + str(status_file) + "\n")
    log_file.write("Tiempo de transferencia: " + str(finish_time - start_time) + "\n")
    log_file.write("Paquetes enviados: " + str(int(file_size/30000)) + "\n")
    log_file.write("Total de bytes enviados: " + str(int(file_size + ((file_size/30000) * 8))) + "\n")
# importar librerias para el manejo del sistema, algoritmos de hash y tiempos
import os
import datetime

# Funcion para generar el archivo de log en el directorio llamado Logs con la informacion determinada en la guia
def write_log_file (file_name, file_size, num_client, status_file, start_time, finish_time, num_package):
    today = datetime.datetime.now()
    name_file = str(today.year) + "-" + str(today.month) + "-" + str(today.day) + "-" + str(today.hour) + "-" + str(today.minute) + "-" + str(today.second) + "-" + str(today.microsecond) + str(file_name[7:8]) + "-log.txt"
    log_file = open("./Logs/" + name_file, "w")
    log_file.write("Nombre del archivo: " + file_name + "\n")
    log_file.write("Tamanio del archivo: " + str((os.path.getsize("./ArchivosRecibidos/"+file_name))) + "\n")
    log_file.write("Cliente que recibe la transeferencia de archivos: " + str(file_name[7:8]) + "\n")
    log_file.write("Estado de entrega del archivo: " + str(status_file) + "\n")
    log_file.write("Tiempo de transferencia: " + str(finish_time - start_time) + "\n")
    log_file.write("Numero de paquetes enviado: " + str(num_package) + "\n")
    log_file.write("Valor total de bytes enviado: " + str(int(file_size + (num_package * 8))) + "\n")
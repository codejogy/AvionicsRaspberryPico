# Desarrollo de computadora en Python
# Variables
from variables import Opciones
from time import time, sleep

def bienvenidaString():
    print("Bienvenido a la computadora de vuelo")
    print("Selecciona la opcion deseada")

def listaString():
    print(f"{Opciones.LECTURADATOS.value}. Lectura de datos")
    print(f"{Opciones.ENVIOINFO.value}. Envio de info a Xbee")
    print(f"{Opciones.OPCIONES.value}. Opciones")
    print(f"{Opciones.SALIR.value}. Salir")

def lecturaDatos():
    import serial
    print("****Usar CTRL+C para terminar bucle****")
    with serial.Serial("com6",baudrate=9600,timeout=5) as ser:
        try:
            while True:
                datosRaw = ser.read_until(expected='><'.encode('utf-8')) 
                print(f"{datosRaw.decode('utf-8')}")
        except KeyboardInterrupt:
            print("Bucle interrumpido, regresando al menu principal")

def opciones():
    # TODO:
    pass

def envioInfo():
    #TODO:
    pass

def salir():
    #TODO:
    pass

def seleccionarOpcion():
    opcion = 0
    while True:
        while True:
            try:
                opcion = int(input())
                break
            except ValueError:
                print("Escribe un número correcto")
                listaString()
                
        match opcion:
            case (Opciones.LECTURADATOS.value):
                print("######## Lectura de datos #########")
                lecturaDatos()
            case (Opciones.ENVIOINFO.value):
                print("######## Enviar Informacion a XBEE #########")
                envioInfo()
            case (Opciones.OPCIONES.value):
                print("######## Opciones #########")
                opciones()
            case (Opciones.SALIR.value):
                print("######## Saliendo #########")
                quit()
            case _:
                print("Selecciona alguna de las opciones")

        listaString()

if __name__ == "__main__":
    bienvenidaString()
    listaString()
    seleccionarOpcion()


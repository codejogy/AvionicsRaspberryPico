# Programa generado para testear el user interface que permita
# obtener bytes, mandar bytes, salirse del menu
from serial import Serial
from time import time,sleep
import sys, os

xbee = Serial("COM8",9600,timeout=5)
counter = time()+5
def main():
    while True:
        #TODO: Generar un menu con 
        # 1. Recibir información
        # 2. Mandar información
        # Abortar en cualquier opción con tecla
        # 3. Salir del programa
        print("#### Menú Principal ####")
        print("Puedes salir de cualquier menu presionando Backspace")
        print("1. Recibir Información")
        print("2. Mandar información")
        print("3. Salir del programa")
        print("Selecciona un número.")
        # Error catching
        try:
            userInput = int(input())
        except ValueError:
            print("Escribe un numero válido")
            continue
        # Identificar que seleccionó el usuario
        match userInput:
            case 1:
                receive()
            case 2:
                send()
            case 3:
                exit()
            case _:
                print("Escribe 1, 2 o 3 y presiona Enter")
        sleep(1)
        if time() > counter: # Si pasa mucho tiempo salir del programa
            break


def receive():
    """Obtener información del Xbee que está en el Raspberry Pi Pico"""
    # print("TODO")
    while True:
        line = xbee.readline()
        print(line)
        sleep(1)
        if time() > counter:
            break

def send():
    """Mandar información hacía el Xbee que está en el Raspberry Pi Pico"""
    # print("TODO")
    while True:
        inp = input(">:")
        xbee.write(inp.encode())
        sleep(1)
        if time() > counter:
            break

def exit():
    """Salir del programa"""
    sys.exit("Saliendo...")

if __name__ == "__main__":
    main()

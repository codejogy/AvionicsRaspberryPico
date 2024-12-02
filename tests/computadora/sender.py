# Programa generado para testear el envío de bytes al Raspberry Pi
from serial import Serial
from time import time,sleep

xbee = Serial("COM8",9600,timeout=5)
counter = time()+5

while True:
    xbee.write("Hola desde la computadora".encode())
    sleep(1)
    if time() > counter:
        break


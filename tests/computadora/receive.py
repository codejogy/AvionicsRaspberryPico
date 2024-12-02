# Programa generado para recibir bytes (lineas) desde el Raspberry Pi
from serial import Serial
from time import time,sleep

xbee = Serial("COM8",9600,timeout=5)

counter = time()+5
while True:
    line = xbee.readline()
    print(line)
    sleep(1)
    if time() > counter:
        break


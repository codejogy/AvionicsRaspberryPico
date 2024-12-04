from machine import UART, Pin
from utime import sleep
from time import time


tiempo = 100 # Segundos hasta terminar el programa
# Leer UART 
# uart = UART(1,baudrate=9600, tx=Pin(8),rx=Pin(9))
uart = UART(0,baudrate=9600,tx=Pin(12),rx=Pin(13))
# uart = UART(0,baudrate=9600)
sleep(0.1)
timeout = time()+tiempo
while True:
    print("Hello World from Raspberry Pi Pico\n\n".encode())
    uart.write("Hello World from Raspberry Pi Pico\n\n".encode())
    if time() > timeout:
        break
    sleep(1)


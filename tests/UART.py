# Programa que inicializa el sensor GPS que necesita UART
from machine import UART, Pin
from utime import sleep
from time import time

# Leer UART del GPIO1
uart = UART(1,baudrate=9600,tx=Pin(4),rx=Pin(5))
# Inicializar con los valores predeterminados
print(uart)
# Asignar el LED
# led = Pin("LED",Pin.OUT)

# Prender LED
# led.on()
timeout = time()+8
while True:
    print(uart.read())
    print(uart.any())
    print(uart.readline())
    # print(uart.readline())
    if time() > timeout:
        break
    sleep(0.5)


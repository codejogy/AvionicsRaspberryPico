from machine import UART, Pin
from utime import sleep
from time import time


# Leer UART 
uart = UART(0,baudrate=9600,tx=Pin(12),rx=Pin(13))
sleep(1)
timeWorking = 10
timeout = time()+timeWorking
while True:
    print(uart.readline())
    if time() > timeout:
        break
    sleep(1)


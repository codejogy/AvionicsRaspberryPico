import machine
from utime import sleep
from time import time

led = machine.Pin(25,machine.Pin.OUT)
timeout = time()+3
while True:
    led.toggle()
    if time() > timeout:
        break
    sleep(1)

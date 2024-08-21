# Testeando el BME280

from machine import I2C, Pin
from utime import time, sleep

i2c = I2C(0,scl=Pin(1),sda=Pin(0))
time_timeout = time()+3
while True:
    devices = i2c.scan()
    if devices:
        for device in devices:
            print(hex(device))
    sleep(0.5)
    if time() == time_timeout:
        print(i2c)
        break

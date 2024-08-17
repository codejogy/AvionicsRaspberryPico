# Testeando el BME280
# BME280 tiene un address que es 0x76

from machine import I2C, Pin
from utime import time, sleep, sleep_ms

i2c = I2C(0,scl=Pin(1),sda=Pin(0))
# And a short delay to wait until the I2C port has finished activating.
sleep_ms(100)
BMEADDRESS = 0x76
BMEADDRESSWRITE = 0xEC
time_timeout = time()+3
while True:
    # To read, first write
    readFromMemory:bytes = i2c.readfrom_mem(BMEADDRESS,0xF7,5,addrsize=8)
    # bytearray(readFromMemory)
    print(readFromMemory)
    sleep(0.5)
    if time() == time_timeout:
        print(i2c)
        break

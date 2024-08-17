# Testeando el BME280
# BME280 tiene un address que es 0x76

from machine import I2C, Pin
from utime import time, sleep, sleep_ms
from bme280_float import BME280

i2c = I2C(0,scl=Pin(1),sda=Pin(0))
# And a short delay to wait until the I2C port has finished activating.
bme = BME280(i2c=i2c)
while True:
    print(bme.values)
    print(bme.dig_H4,bme.dig_H5,bme.dig_H6)
    raw_data=[0,0,0]
    bme.read_raw_data(raw_data)
    print(raw_data)
    print("dig_ t1,t2,t3",bme.dig_T1,bme.dig_T2,bme.dig_T3)
    print("dig_ h",bme.dig_H1,bme.dig_H2,bme.dig_H3,bme.dig_H4,bme.dig_H5,bme.dig_H6)
    sleep(1)


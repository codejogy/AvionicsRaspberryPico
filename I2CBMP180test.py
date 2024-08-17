from I2CBMP180LIB import BMP180
from machine import I2C, Pin

i2c = I2C(0,scl=Pin(1),sda=Pin(0))

bmp180 = BMP180(i2c)
print("VALORES",bmp180.compvaldump())
print(bmp180.pressure)
print(bmp180.altitude)


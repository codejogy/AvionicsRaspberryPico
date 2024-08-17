from machine import Pin, I2C
from utime import sleep_ms
from struct import unpack
from math import log


i2c = I2C(id=0, scl=Pin(1), sda=Pin(0))


# print(list(map(hex,i2c.scan())))
# 0x77 Address BME180
ADDRESS = 0x77
# id = i2c.readfrom_mem(ADDRESS,0xD0,1)
# print(id.hex()) 

# Read calib data
calibBytes = bytearray(22)
i2c.readfrom_mem_into(ADDRESS,0xAA,calibBytes)
# Works with big endian, as it should
calibData = unpack(">hhhHHHhhhhh",calibBytes)
AC1,AC2,AC3,AC4,AC5,AC6,B1,B2,MB,MC,MD = calibData
# Read temperatura values
_tempWrite = bytearray(1)
_tempWrite[0]=0x2E
i2c.writeto_mem(ADDRESS,0xF4,_tempWrite)
sleep_ms(26)
tempBytes = bytearray(2)
i2c.readfrom_mem_into(ADDRESS,0xF6,tempBytes)
ut = (tempBytes[0] << 8) + tempBytes[1]

# _oss = 0b00 # One oversampling
# _oss = 0b01 # two times oversampling
_oss = 0b11 # 8 times oversampling

# Read pressure values
_presWrite = bytearray(1)
_presWrite[0]=0x34 + (_oss << 6)
i2c.writeto_mem(ADDRESS,0xF4,_presWrite)
# Using 26 seconds just as Page 21 BMP180 datasheet says for oversampling
sleep_ms(26)
presBytes = bytearray(3)
i2c.readfrom_mem_into(ADDRESS,0xF6, presBytes)
presBytes = unpack("BBB",presBytes)
up = ((presBytes[0] << 16) + (presBytes[1] << 8) + presBytes[2])>>(8-_oss)
# DEBUGGING
# print("DEBUGGING")
# [print(hex(presByte)) for presByte in presBytes]

# DEBUGGING (BORRAR POST DEBUGGING)
# ut = 27898
# up = 23843
#################
# from struct import unpack as unp
# AC1 = unp('>h', i2c.readfrom_mem(ADDRESS, 0xAA, 2))[0]
# AC2 = unp('>h', i2c.readfrom_mem(ADDRESS, 0xAC, 2))[0]
# AC3 = unp('>h', i2c.readfrom_mem(ADDRESS, 0xAE, 2))[0]
# AC4 = unp('>h', i2c.readfrom_mem(ADDRESS, 0xB0, 2))[0]
# AC5 = unp('>h', i2c.readfrom_mem(ADDRESS, 0xB2, 2))[0]
# AC6 = unp('>h', i2c.readfrom_mem(ADDRESS, 0xB4, 2))[0]
# B1 = unp('>h', i2c.readfrom_mem(ADDRESS, 0xB6, 2))[0]
# B2 = unp('>h', i2c.readfrom_mem(ADDRESS, 0xB8, 2))[0]
# MD = unp('>h', i2c.readfrom_mem(ADDRESS, 0xBE, 2))[0]
# MC = unp('>h', i2c.readfrom_mem(ADDRESS, 0xBC, 2))[0]
# MB = unp('>h', i2c.readfrom_mem(ADDRESS, 0xBA, 2))[0]
#################
# AC1 = 408
# AC2 = -72
# AC3 = -14383
# AC4 = 32741
# AC5 = 32757
# AC6 = 23153
# B1 = 6190
# B2 = 4
# MB = -32767
# MC = -8711
# MD = 2868

# Calculate true temperature
x1 = (ut-AC6)*AC5//32_768
x2 = MC*2_048//(x1+MD)
b5 = x1 + x2
t = (b5+8)//16


#Calculate true pressure
b6 = b5-4000
x1 = (B2*(b6*b6/4096))//2048
x2 = AC2*b6//2048
# print("X1 first time",x1,"X2 first time",x2) # DEBUGGING
x3 = int(x1+x2)
b3 =(((AC1*4+x3)<<_oss)+2)//4
# print("X3 first time",x3,"B3 first time",b3) # DEBUGGING
x1 = AC3*b6//8192
x2 = (B1*(b6*b6//4096))//65536
x3 = ((x1+x2)+2)//4
b4 = AC4*(x3+32768)//32768
b7 = (up-b3)*(50_000 >> _oss)
p = (b7*2)//b4 if b7 < 0x80_000_000 else (b7//b4)*2
x1 = (p//256)*(p//256)
x1 = (x1*3038)//65536
x2 = (-7357*p)//65536
p = p + (x1+x2+3791)//16

# Correction for pressure (103206~ reading)
# 100910 pressure in my place right now
# p_correction = 103206-100910

# p = p - p_correction
# Volver presion a 0 para calcular altitud desde un punto fijo
# p = p -103225
# Calculate altitude
po = 101325
altitude = 44330*(1-(p/po)**(1/5.255))
# Volver 0
altitude = altitude + 157.4
# altitude = -7990.0*log(p/po)


# print("ut",ut,"up",up)
print("Temperatura:",t/10,",","Presion:",p,"Pa")
print("Altitud en metros",altitude)

# Debugging
# print("B5",b5,)
# print("B6",b6)
# print("X1",x1,"\nx2",x2)


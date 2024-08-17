# Testeando el BME280
# BME280 tiene un address que es 0x76

from machine import I2C, Pin
from utime import time, sleep, sleep_ms
from struct import unpack, pack

i2c = I2C(0,scl=Pin(1),sda=Pin(0))
BMEADDRESS = 0x76
time_timeout = time()+3
_l8_bytearray = bytearray(8)
# Configurar humedad para que se lea
humedad_configs = bytearray(1) # Necesario que sea en modo de bytes
_humedad_address = 0xF2  # Address humedad
_control_humedad:binary = 0b001 # Oversampling x1
humedad_configs[0]=_control_humedad
i2c.writeto_mem(BMEADDRESS,_humedad_address,humedad_configs)
# Configurar temperatura, presion y modo
tempe_pres_modo_configs = bytearray(1)
tempe_pres_modo_address = 0xF4
_tempe:binary = 0b001 # Oversampling x 1 para temperatura
_pres:binary = 0b001 # Oversmapling x1 para temperatura
_mode:binary = 0b11 # Modo normal
# _mode:binary = 0b01 # Modo forced 
# Concatenar tempe, pres y mode. Tempe tiene los bits 7,6,5; Pres tiene 4,3,2; mode tiene 1,0
# El bit más significativo va a la izquierda
tempe_pres_modo_configs[0] = _tempe << 5 | _pres << 2 | _mode
# Basicamente: tempe se recorre a la izq 5 veces, se aplica or
    # Es 5 veces a la izq dado que _tempe contiene los bits 7,6,5. Debe dar 5 espacios para los bits 4 al 0, son 5
# _pres se recorre 2 veces a la izquierda después que tempe lo hizo, se aplica or
    # Es 2 veces ya que _pres contiene los bits 4,3,2. Dando espacio para los bits 1 y 0, que son 2
# _mode se aplica en or después que ambos operadores se recorrieron.
# De esta manera se concatena
# Empezar a leer
i2c.writeto_mem(BMEADDRESS,tempe_pres_modo_address,tempe_pres_modo_configs)

# Leer valores de registro del 0x88 al 0x9F (24 valores incluyendo el 0x88)
calibration_values_88_9f = i2c.readfrom_mem(BMEADDRESS, 0x88, 24)
# Leer valor de registro A1
calibration_values_a1 = i2c.readfrom_mem(BMEADDRESS,0xA1, 1)
# Leer valor de registro E1 a E6
calibration_values_e1_e7 = i2c.readfrom_mem(BMEADDRESS,0xE1, 7)
# Obtener los valores de compensación
# < dice que es little endian, para más info https://docs.python.org/3/library/struct.html
calibration_88_9f = unpack("<H2hH8h", calibration_values_88_9f)
calibration_a1 = unpack("<B",calibration_values_a1)
# 0xE5 comparte bits entre dos valores, se toman bytes en arreglo especifico
calibration_e1_e7 = unpack("<hBbhb",calibration_values_e1_e7)

dig_T1,dig_T2,dig_T3,dig_P1,dig_P2,dig_P3,dig_P4,dig_P5,dig_P6,dig_P7 \
,dig_P8,dig_P9 = calibration_88_9f

dig_H1 = calibration_a1[0]

dig_H2,dig_H3,dig_H4,dig_H5,dig_H6 = calibration_e1_e7
# Dado que en el datasheet dig_H4 y H5 se toman de bits especificos
# En este caso, H4 se tomó como un signed char para tomar el primer byte 0xE4
dig_H4 = dig_H4 << 4 | (dig_H5 & 0b1111)
# E5 es el LSB y E6 el MSB de dig_H5
dig_H5 = dig_H5 >> 4

t_fine = 0
def calibrar_temperatura(tempe_bruta):
    """La temperatura se calibrará conforme los valores del BME"""
    # Extraida la formula del datasheet BME280
    # adc_T = tempe_bruta
    # var1 = ((((adc_T >3) - (dig_T1<<1))) * (dig_T2)) >> 11
    # var2 = (((((adc_T>>4) - dig_T1) * ((adc_T>>4) - dig_T1)) >> 12) * dig_T3) >> 14;
    # global t_fine 
    # t_fine = var1+var2
    # temperatura_calibrada = (t_fine * 5 + 128) >> 8
    raw_temp = tempe_bruta
    var1 = (((raw_temp // 8) - (dig_T1 * 2)) * dig_T2) // 2048
    var2 = (raw_temp // 16) - dig_T1
    var2 = (((var2 * var2) // 4096) * dig_T3) // 16384
    global t_fine
    t_fine = var1 + var2
    temperatura_calibrada = (t_fine * 5 + 128) // 256
    return temperatura_calibrada

def calibrar_presion(presion_bruta):
    """La presion se calibrará conforme los valores del BME"""
    global t_fine
    var1 = (t_fine) - 128000;
    var2 = var1 * var1 * dig_P6
    var2 = var2 + ((var1*dig_P5)<<17)
    var2 = var2 + (dig_P4<<35)
    var1 = ((var1 * var1 * dig_P3)>>8) + ((var1 * dig_P2)<<12)
    var1 = (((1<<47)+var1))*(dig_P1)>>33
    if var1 == 0:
        return 0 # avoid exception caused by division by zero
    
    p = 1048576-presion_bruta
    p = (((p<<31)-var2)*3125)/var1
    p = int(p)
    var1 = (dig_P9 * (p>>13) * (p>>13)) >> 25
    var2 = (dig_P8 * p) >> 19
    p = ((p + var1 + var2) >> 8) + (dig_P7<<4)
    return p

def calibrar_humedad(humedad_bruta):
    """La humedad se calibrará conforme los valores del BME"""
    global t_fine 
    v_x1_u32r = (t_fine - 76800)
    v_x1_u32r = (((((adc_H << 14) - (dig_H4 << 20) - (dig_H5 * v_x1_u32r)) + 16384) \
        >> 15) * (((((((v_x1_u32r * dig_H6) >> 10) * (((v_x1_u32r * dig_H3) >> 11) \
       + 32768)) >> 10) + 2097152) * dig_H2 + 8192) >> 14))
    v_x1_u32r = (v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) \
        * dig_H1) >> 4))
    # v_x1_u32r = (v_x1_u32r < 0 ? 0 : v_x1_u32r)
    # v_x1_u32r = (v_x1_u32r > 419430400 ? 419430400 : v_x1_u32r)
    # De C a Python 
    v_x1_u32r = 0 if v_x1_u32r < 0 else v_x1_u32r
    v_x1_u32r = 419430400 if v_x1_u32r > 419430400 else v_x1_u32r
    return (v_x1_u32r>>12)

# Esperar un poco mientras se termina de configurar
sleep(0.5)
while True:
    # Empezar el modo normal
    # Leer valores de memoria y almacenarlos en _l8_bytearray
    i2c.readfrom_mem_into(BMEADDRESS, 0xF7, _l8_bytearray)
    readout = _l8_bytearray
    # Presión sin procesar
    # MSB -> Most Significant BYTE en el caso de los address que arroja I2C
    # 20 bits = MSB + LSB + XLSB(4bits), todo concatenado
    presion_bruta = (_l8_bytearray[0]<<16) | (_l8_bytearray[1]<<8) | (_l8_bytearray[2]>>4)
    temperatura_bruta =(_l8_bytearray[3]<<16) | (_l8_bytearray[4]<<8)| (_l8_bytearray[5]>>4)
    humedad_bruta =(_l8_bytearray[6]<<8) | (_l8_bytearray[7]) 
    print(readout)
    for byte in readout:
        print("Byte:", hex(byte), end=" ")
    print()
    print("Presion:",presion_bruta,"Temperatura:",temperatura_bruta,"Humedad:",humedad_bruta)
    print("T calib: ",calibrar_temperatura(temperatura_bruta)/10000, \
        "P calib:",calibrar_presion(presion_bruta), \
        "H calib:",calibrar_temperatura(humedad_bruta))
    sleep(0.3)
    if time() > time_timeout:
        break
# for byte in readout:
#     print(hex(byte))

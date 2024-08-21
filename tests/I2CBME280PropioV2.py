from machine import Pin, I2C
from struct import unpack

i2c = I2C(0,scl=Pin(1),sda=Pin(0))

ADDRESS = 0x76

# Read Calibration Data


calibration_values = i2c.readfrom_mem(ADDRESS,0x88,26)
dig_T1,dig_T2,dig_T3,dig_P1,dig_P2,dig_P3,dig_P4,\
dig_P5,dig_P6,dig_P7,dig_P8,dig_P9,_,dig_H1=unpack("<HhhHhhhhhhhhBB", calibration_values)

calibration_values = i2c.readfrom_mem(ADDRESS,0xE1,7)
dig_H2,dig_H3,_E4,_E5,_E6,dig_H6=unpack("<hBbbbb",calibration_values)

dig_H4=(_E4<<4) | (_E5 & 0b1111)
dig_H5=(_E6<<4) | (_E5 >> 4)
# # DEBUGGING DELETE ###########
# print(_E4,_E5,_E6)
# ##############################
# Register controls


_ctrl_hum = 0xF2
_status = 0xF3
_ctrl_meas = 0xF4
_config = 0xF5
_p_t_h_bytes = bytearray(8)
_ctrl_hum_byte = bytearray(1)
_ctrl_meas_byte = bytearray(1)

# Oversampling and mode config
OVERSAMPLING = 0b010 # Oversampling: 001 x1,010 x2, 011 x4, 100 x8, 101 x16
MODE = 0b10 # Mode: 00 Sleep, 01 or 10 Forced, 11 Normal mode

_ctrl_hum_byte[0]=OVERSAMPLING
_ctrl_meas_byte[0]= OVERSAMPLING << 5 | OVERSAMPLING << 2 | MODE

i2c.writeto_mem(ADDRESS,_ctrl_hum, _ctrl_hum_byte)
i2c.writeto_mem(ADDRESS,_ctrl_meas,_ctrl_meas_byte)
    
# Read temperature, pressure and humity

i2c.readfrom_mem_into(ADDRESS, 0xF7, _p_t_h_bytes)

# Temperature, pressure and humity raw values

u_p = ((_p_t_h_bytes[0]<<16) | (_p_t_h_bytes[1]<<8) | (_p_t_h_bytes[2]))>>4
u_t = ((_p_t_h_bytes[3]<<16) | (_p_t_h_bytes[4]<<8) | (_p_t_h_bytes[5]))>>4
u_h = (_p_t_h_bytes[6]<<8) | (_p_t_h_bytes[7])

# Compensation formulas (int)

t_fine = 0

#   Compensate temperature (copied from datasheet)
adc_T = u_t

var1 = ((((adc_T>>3) - (dig_T1<<1))) * dig_T2) >> 11
var2 = (((((adc_T>>4) - dig_T1) * ((adc_T>>4) - dig_T1))>> 12) * dig_T3) >> 14;
t_fine = var1 + var2;
T = (t_fine * 5 + 128) >> 8;

#   Compensate pressure (copied from datasheet)
adc_P = u_p

var1 = (t_fine) - 128000;
var2 = var1 * var1 * dig_P6;
var2 = var2 + ((var1*dig_P5)<<17);
var2 = var2 + ((dig_P4)<<35);
var1 = ((var1 * var1 * dig_P3)>>8) + ((var1 * dig_P2)<<12);
var1 = ((((1)<<47)+var1))*(dig_P1)>>33;
if (var1 == 0):
    p = 0;  # avoid exception caused by division by zero
else:
    p = 1048576-adc_P;
    p = (((p<<31)-var2)*3125)//var1;
    var1 = ((dig_P9) * (p>>13) * (p>>13)) >> 25;
    var2 = ((dig_P8) * p) >> 19;
    p = ((p + var1 + var2) >> 8) + ((dig_P7)<<4);

P = p

#   Compensate humity (Copied from datasheet)
adc_H = u_h

v_x1_u32r = (t_fine - 76800);
v_x1_u32r = (((((adc_H << 14) - (dig_H4 << 20) - (dig_H5 * \
v_x1_u32r)) + 16384) >> 15) * (((((((v_x1_u32r * \
dig_H6) >> 10) * (((v_x1_u32r * dig_H3) >> 11) + \
32768)) >> 10) + 2097152) * dig_H2 + \
8192) >> 14))
v_x1_u32r = v_x1_u32r - (((((v_x1_u32r >> 15) * (v_x1_u32r >> 15)) >> 7) * \
dig_H1) >> 4)
# v_x1_u32r = (v_x1_u32r < 0 ? 0 : v_x1_u32r);
v_x1_u32r = 0 if v_x1_u32r < 0 else v_x1_u32r
# v_x1_u32r = (v_x1_u32r > 419430400 ? 419430400 : v_x1_u32r);
v_x1_u32r = 419430400 if v_x1_u32r > 419430400 else v_x1_u32r
v_x1_u32r = v_x1_u32r >> 12
H = v_x1_u32r
if v_x1_u32r <= 0:
    H = 0
elif v_x1_u32r >= 100*1024:
    H = 100*1024


# Printing
# print("Valores descompensados")
# print("Temperatura",u_t,"Presion",u_p,"Humedad",u_h)
# print("Valores compensados")
print("Temperatura (C)",T/100,"Presion (Pa)",P/256,"Humedad (%)",H/1024)
# print("H4, H5",dig_H4,dig_H5)
# print("dig_ t1,t2,t3",dig_T1,dig_T2,dig_T3)
# print("dig_ h",dig_H1,dig_H2,dig_H3,dig_H4,dig_H5,dig_H6)

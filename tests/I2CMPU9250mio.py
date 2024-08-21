from machine import Pin, I2C
from utime import sleep_ms
from struct import unpack

i2c = I2C(0, scl = Pin(1), sda = Pin(0))

print(list(map(hex,i2c.scan())))

ADDRESS = 0x68 # FOR ACCELEROMETER AND GYROSCOPE
ADDRESS_2 = 0xC # FOR MAGNETOMETER

# SAVE ALL SELF TEST

self_tests = i2c.readfrom_mem(ADDRESS, 0x00, 6)

# OFFSET

# POWER MANAGEMENT

_pwr_mgmt_1_address = 107
_h_reset = 0b1000_0000 # Reset everything
_pwr_mgmt = bytearray(1)
_pwr_mgmt[0] = _h_reset
i2c.writeto_mem(ADDRESS, _pwr_mgmt_1_address,_pwr_mgmt)
sleep_ms(10)
#   Add clock settings
_pwr_mgmt[0] = 0b1 
i2c.writeto_mem(ADDRESS, _pwr_mgmt_1_address,_pwr_mgmt)

# CONFIG

# _config_address = 26 # In decimal
# _fifo_mode = 0b00 # When the data is fullin FIFO, replace it for new one. bit 6
# _ext_sync_set = 0b00 # No FSYNC functions (i dont' know how to use them). bit [5:3]
# _dlpf_cf = 0b00 # DLPF is a low pass filter, not needed right now. 
# # for more info https://forum.arduino.cc/t/activating-low-pass-filter-on-mpu6050/475211. bit[2:0]
# config_bytes = bytearray(1)
# config_bytes[0] = 0<<7 | _fifo_mode <<6 | _ext_sync_set << 3 | _dlpf_cf
#
# i2c.writeto_mem(ADDRESS,_config_address ,config_bytes)
# # Add delay after writing for MPU response
# sleep_ms(5)
# config = i2c.readfrom_mem(ADDRESS,0x1A,1)

# GYRO CONFIG
_gyro_config_address = 27

_zgyro_cten = 0b00
_xgyro_cten = 0b00
_ygyro_cten = 0b00

_gyro_fs_sel= 0b00 # 00 -> +250°/s, 01 -> +500 °/s, 10 -> 1000 °/s, 11 -> 2000 °/s
factor_gyro_250 = 131 # LSB/(°/s)
factor_gyro_500 = 65.5 # LSB/(°/s)
factor_gyro_1000= 32.8 # LSB/(°/s)
factor_gyro_2000= 16.4 # LSB/(°/s)
_ = 0b00
_fchoice_b = 0b00 # No DLPF
gyro_config_bytes = bytearray(1)
gyro_config_bytes[0] = _xgyro_cten << 7 | _ygyro_cten << 6 | _zgyro_cten << 5 | \
    _gyro_fs_sel << 3 | _ << 1 | _fchoice_b 

i2c.writeto_mem(ADDRESS, _gyro_config_address, gyro_config_bytes)
# Add delay after writing for MPU response
sleep_ms(5)

# ACCELEROMETER CONFIG 1
_accel_reg1 = 28

_ax_st_en = 0b00
_ay_st_en = 0b00
_az_st_en = 0b00

ACCEL_FS_SEL = 0b11 # Scale: ±2g (00), ±4g (01), ±8g (10), ±16g (11)
factor2g = 16384 # scale factor LSB/g
factor4g = 8192 # scale factor LSB/g
factor8g = 4096 # scale factor LSB/g
factor16g = 2048 # scale factor LSB/g

_ = 0b00
accel_config_bytes = bytearray(1)
accel_config_bytes[0] = _ax_st_en << 7 | _ay_st_en << 6 | _az_st_en << 5 | \
    ACCEL_FS_SEL << 3 | _ 

i2c.writeto_mem(ADDRESS,_accel_reg1 , accel_config_bytes)

# ACCELEROMETER CONFIG 2
# _accel_reg2 = 29
#
# _ = 0b00
# _accel_fchoice_b = 0
# _a_dlpfcfg = 0b00 
# accel_config_bytes_2 = bytearray(1)
# accel_config_bytes_2[0] = _ << 6| _ << 4 | _accel_fchoice_b << 3 | \
#     _a_dlpfcfg
#
# i2c.writeto_mem(ADDRESS,_accel_reg2 , accel_config_bytes_2)

# FIFO ENABLE
# _fifo_enable_reg = 35
#
# _temp_out = 0b1 # Enable temperature
# _gyro_xout = 0b1 # Enable gyroscope x
# _gyro_yout = 0b1 # Enable gyroscope y
# _gyro_zout = 0b1 # Enable gyroscope z
# _accel = 0b1 # Enable acceleration
# slv_2 = 0b0 # Disable Slave 2
# slv_1 = 0b0 # Disable Slave 1
# slv_0 = 0b0 # Disable Slave 0
#
# fifo_config_bytes = bytearray(1)
# fifo_config_bytes[0] = _temp_out << 7 | _gyro_xout << 6 | _gyro_yout << 5 | _gyro_zout << 4 | _accel << 3 | slv_2 << 2 | slv_1 << 1 | slv_0
#
# i2c.writeto_mem(ADDRESS,_fifo_enable_reg,fifo_config_bytes)
# fifo = i2c.readfrom_mem(ADDRESS, _fifo_enable_reg,1)

# USER CONTROL
# _user_ctrl_register = 106
# _user_ctrl_bytes = bytearray(1)
#
# _ = 0b0
# _fifo_en = 0b01 # Enable FIFO operation mode (idk what will happen)
# _i2c_mst_en = 0b0 # Disable i2c
# _i2c_if_dis = 0b0 # Not enable SPI
# __ = 0b00
# _fifo_rst = 0 # Not reset FIFO module
# _i2c_mst_rst = 0 # Not reset I2C Master
# _sig_cond_rst = 0 # Not reset any digital signal path
#
# _user_ctrl_bytes[0] = _ << 7 | _fifo_en << 6 | _i2c_mst_en << 5 | _i2c_if_dis << 4 | _ << 3 | _fifo_rst << 2 | _i2c_mst_rst << 1 | _sig_cond_rst
# i2c.writeto_mem(ADDRESS,_user_ctrl_register, _user_ctrl_bytes)

# FIFO COUNT
# _fifo_countH_register = 114 # HIGH BYTE
# _fifo_countL_register = 115 # LOW BYTE
# _fifo_count_bytes=bytearray(2)
# i2c.readfrom_mem_into(ADDRESS, _fifo_countH_register,_fifo_count_bytes)
# fifo_count = (_fifo_count_bytes[0] & 11111) | (_fifo_count_bytes[1])


# MEASUREMENTS (accel, temp and gyro)
_measurements_register_1 = 59
_meas_bytes = bytearray(6+2+6)

i2c.readfrom_mem_into(ADDRESS,_measurements_register_1, _meas_bytes)
# accel_xout = _meas_bytes[0]<<8 | _meas_bytes[1]
# accel_yout = _meas_bytes[2]<<8 | _meas_bytes[3]
# accel_zout = _meas_bytes[4]<<8 | _meas_bytes[5]
#
# temperature = _meas_bytes[6]<<8 | _meas_bytes[7]
#
# gyro_xout = _meas_bytes[8]<<8 | _meas_bytes[9]
# gyro_yout = _meas_bytes[10]<<8 | _meas_bytes[10]
# gyro_zout = _meas_bytes[11]<<8 | _meas_bytes[12]

accel_xout,accel_yout,accel_zout, temperature,gyro_xout,gyro_yout,gyro_zout = \
unpack(">hhhhhhh", _meas_bytes)
 
# gyro_xout,gyro_yout,gyro_zout = unpack(">hhh",_meas_bytes[8:])
### MAGNETOMETER AK8963 ###
ADRESS = ADDRESS_2 # Just to be sure

#  CONTROL 1
_magn_control_1_address = 0xA
_magn_control_1_byte = bytearray(1)
_control_mode = 0b0010 # Continuous measurements mode
_control_bit = 0b1 # 16 bit

_magn_control_1_byte[0] = _control_bit << 4 | _control_mode
i2c.writeto_mem(ADDRESS_2,_magn_control_1_address,_magn_control_1_byte)

# CONTROL 2
# _magn_control_2_address = 0xB
# _magn_control_2_byte = bytearray(1)
#
# _magn_control_2_byte[0]=0b1
# i2c.writeto_mem(ADDRESS_2, _magn_control_2_address, _magn_control_2_byte)
# sleep_ms(10)

# MEASUREMENT DATA
_meas_magn_register = 0x03
_status2_register = 0x09 # Status 2 needs to be read to read new measurements
_meas_magn_bytes = bytearray(6)

i2c.readfrom_mem_into(ADDRESS_2,_meas_magn_register,_meas_magn_bytes)
sleep_ms(10)
i2c.readfrom_mem(ADDRESS_2,_status2_register, 1) # Status 2 needs to be read
# Signed short for every axis in little endian
magnetic_x = _meas_magn_bytes[1]<<8 | _meas_magn_bytes[0]
magnetic_y = _meas_magn_bytes[3]<<8 | _meas_magn_bytes[2]
magnetic_z = _meas_magn_bytes[5]<<8 | _meas_magn_bytes[4]
magnetic_x,magnetic_y,magnetic_z = unpack("<hhh", _meas_magn_bytes)

# Printing

    # DEVICE ID magn
# print("Magnetometer ID",i2c.readfrom_mem(ADDRESS,0x00,1)[0])
# # Is not giving 0x48, so the magnetometer could not work
#     # INFORMATION magn
# print("Information Magnetometer:",i2c.readfrom_mem(ADDRESS, 0x01,1)[0])
# print("Config:",config)
# print("Fifo:",fifo[0])
# print("User control:",_user_ctrl_bytes[0])
# print("Fifo count:",fifo_count)

print("Accel",accel_xout,accel_yout,accel_zout,"Temperatura",temperature,"Giroscopio",gyro_xout,gyro_yout,gyro_zout) 
factor = factor16g
factor_gyro = factor_gyro_250
print("AX",accel_xout/factor,"AY",accel_yout/factor,"AZ",accel_zout/factor)
print("Temperature",temperature/100)
print("GX",gyro_xout/factor_gyro,"GY",gyro_yout/factor_gyro,"GZ",gyro_zout)

print(magnetic_x,magnetic_y,magnetic_z)

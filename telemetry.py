# Get information from BMP180, BME280, MPU-9250 and NEO-6M
# TODO: Agregar NEO-6M
from machine import Pin, I2C
from bmp180 import BMP180
from bme280_int import BME280
from mpu9250 import MPU9250
from utime import time,sleep_ms

i2c = I2C(id=0,sda=Pin(0),scl=Pin(1))

bmp180 = BMP180(i2c)
bme280 = BME280(i2c=i2c)
mpu9250 = MPU9250(i2c)

# Generate a timeout value
time_start = time()
TIMEOUT = 8 # seconds before stoping the program

if __name__ == "__main__":
    while True:
        # BMP180 Values
        pressure_bmp180 = bmp180.pressure
        temperature_bmp180 = bmp180.temperature
        altitude_bmp180 = bmp180.altitude

        # BME280 Values
        temperature_bme280, pressure_bme280, humidity_bme280 = bme280.read_compensated_data()
        altitude_bme280 = bme280.altitude

        # MPU9250 Values
        temperature_mpu9250 = mpu9250.temperature
        acceleration_mpu9250 = mpu9250.acceleration
        gyro_mpu9250 = mpu9250.gyro
        magnetic_mpu9250 = mpu9250.magnetic

        print("###Temperature###")
        print(f"{temperature_bmp180},{temperature_bme280},{temperature_mpu9250}")
        print("###Pressure###")
        print(f"{pressure_bmp180},{pressure_bme280}")
        print("###Altitude###")
        print(f"{altitude_bmp180},{altitude_bme280}")
        print("###Humidity###")
        print(f"{humidity_bme280}")
        print("###Acceleration###")
        print(f"{acceleration_mpu9250}")
        print("###Gyroscope###")
        print(f"{gyro_mpu9250}")
        print("###Magnetic###")
        print(f"{magnetic_mpu9250}")
        print()
        print("><")
        sleep_ms(500)

        if time() >= time_start+TIMEOUT:
            break



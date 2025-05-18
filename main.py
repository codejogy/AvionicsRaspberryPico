# INFO: STARTING THE RPPI PICO UART PINS
from machine import UART, Pin
from time import sleep
uart = UART(0,baudrate=9600,tx=Pin(12),rx=Pin(13))
sleep(0.5)

# INFO: START THE TELEMETRY
from telemetry import *

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
    print(f"{temperature_bmp180:.2f},{temperature_bme280:.2f},{temperature_mpu9250:.2f}")
    print("###Pressure###")
    print(f"{pressure_bmp180:.2f},{pressure_bme280:.2f}")
    print("###Altitude###")
    print(f"{altitude_bmp180:.2f},{altitude_bme280:.2f}")
    print("###Humidity###")
    print(f"{humidity_bme280:.2f}")
    print("###Acceleration###")
    print(f"{acceleration_mpu9250[0]:.6f},{acceleration_mpu9250[1]:.6f},{acceleration_mpu9250[2]:.6f}")
    print("###Gyroscope###")
    print(f"{gyro_mpu9250[0]:.6f},{gyro_mpu9250[1]:.6f},{gyro_mpu9250[2]:.6f}")
    print("###Magnetic###")
    print(f"{magnetic_mpu9250[0]:.3f},{magnetic_mpu9250[1]:.3f},{magnetic_mpu9250[2]:.3f}")
    print("><")
    uart.write("###Temperature###\n")
    uart.write(f"{temperature_bmp180},{temperature_bme280},{temperature_mpu9250}\n")
    uart.write("###Pressure###\n")
    uart.write(f"{pressure_bmp180},{pressure_bme280}\n")
    uart.write("###Altitude###\n")
    uart.write(f"{altitude_bmp180},{altitude_bme280}\n")
    uart.write("###Humidity###\n")
    uart.write(f"{humidity_bme280}\n")
    uart.write("###Acceleration###\n")
    uart.write(f"{acceleration_mpu9250}\n")
    uart.write("###Gyroscope###\n")
    uart.write(f"{gyro_mpu9250}\n")
    uart.write("###Magnetic###\n")
    uart.write(f"{magnetic_mpu9250}\n")
    uart.write("><\n")
    sleep_ms(400)

# Pin 12 and pin 13 are initialized to be UART
# LED BLINKS TO SAY ITS STARTED OR RESTARTED
# led = machine.Pin(25,machine.Pin.OUT)
# for i in range(4):
#     led.toggle()
#     sleep(0.1)

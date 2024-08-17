from machine import Pin, ADC
from utime import sleep

# El sensor está en el pin 4
sensor_temperatura = ADC(4)
conversion_factor = 3.3/65535

while True:
    reading = sensor_temperatura.read_u16()*conversion_factor
    temperatura = round(27-(reading-0.706)/0.001721,2)
    print("Temperatura:",temperatura)
    sleep(0.1)

# Programa hecho para un LED que tiene conectado una resistencia

from machine import Pin
from utime import sleep

# Se generará en el pin GP19 una salida
led_pin = Pin(19,Pin.OUT)



while True:
    # El led se mantendrá encendido
    # led_pin.on()
    # print("Led encendido")

    # El led parpadeará
    led_pin.toggle()
    print("Led encendido")
    sleep(0.5)

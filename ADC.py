from machine import ADC
from utime import sleep
# Declarar que el potenciometro está en el pin GPIO26
potenciometro = ADC(26)

while True:
    # Lectura y print de lo que el potenciometro tenga
    print(potenciometro.read_u16())
    # Descansar
    sleep(0.5)
    

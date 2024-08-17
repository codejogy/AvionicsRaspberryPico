import machine
import utime

# Declarar los pines que se usarán
button = machine.Pin(19,machine.Pin.IN, machine.Pin.PULL_UP) # Pin se usará como entrada



while True: # Se genera un ciclo while que dura permanentemente
    # Cuando el botón se presione, imprimirá que lo hizo
    if button.value() == 1:
        print("Boton sin presionar")
    # Cuando no se presione, que no lo está
    else:
        print("Boton presionado")
    # Esperar 500 milisegundos
    utime.sleep_ms(500)

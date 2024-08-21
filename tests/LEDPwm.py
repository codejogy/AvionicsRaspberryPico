from machine import PWM, Pin
from utime import sleep, sleep_ms

led_out = Pin(19,Pin.OUT)


# La frecuencia son los pulsos por segundos que manda, a menor frecuencia, más facil de percibir el PWM
freq = 1000
led_pwm = PWM(led_out,freq=freq)

# Tiene que ser entero, por eso "//"
duty_cicle = 65535//1

while True:
    # Va a ser un dimmer que ira prendiendo poco a poco hasta llegar a su valor maximo
    for duty in range(duty_cicle):
        led_pwm.duty_u16(duty)
        sleep(0.0001)

    for duty in range(duty_cicle,0,-1):
        led_pwm.duty_u16(duty)
        sleep(0.0001)

    # led_pwm.duty_u16(duty_cicle)
    # sleep(1)
    # led_pwm.duty_u16(0)
    # sleep(1)
    # print("Ciclo!")

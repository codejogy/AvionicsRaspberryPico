from machine import Pin
from utime import sleep

# El pin GP19, será de entrada, con resistencia Pulldown
# button_state = Pin(19, Pin.IN, Pin.PULL_UP)
# El pin GP19, será de entrada
button_state = Pin(19, Pin.IN, Pin.PULL_DOWN)
# El pin GP25 sera de salida
led_state = Pin(25, Pin.OUT)


while True:
    if button_state.value() == 1:
        # The button is pressed, then the led will turn on
        led_state.on()
        print(f"Led prendido!, status {led_state.value()}")
    else:
        # The button is not pressed
        led_state.off()
        print(f"Led apagado, status {led_state.value()}")
    # print(button_state)
    sleep(0.1)

from machine import UART, Pin
from time import sleep
uart = UART(0,baudrate=9600,tx=Pin(12),rx=Pin(13))
sleep(0.5)
# Pin 12 and pin 13 are initialized to be UART
# LED BLINKS TO SAY ITS STARTED OR RESTARTED
# led = machine.Pin(25,machine.Pin.OUT)
# for i in range(4):
#     led.toggle()
#     sleep(0.1)
# # Test uart restarted
# uart.write("Hello World from Raspberry Pi Pico\n\n".encode())


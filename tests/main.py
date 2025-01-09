
from machine import UART, Pin
from utime import sleep
from time import time

uart = UART(0,baudrate=9600,tx=Pin(12),rx=Pin(13))

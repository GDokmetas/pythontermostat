from machine import *
import time
import ds18b20
from ds18b20 import ds 
isitma = Pin(0, Pin.OUT)
sogutma = Pin(1, Pin.OUT)
sicak_led = Pin(2, Pin.OUT)
soguk_led = Pin(3, Pin.OUT)
# UART Tanimlama
uart = UART(1, 9600, tx = Pin(8), rx = Pin(9))
# ayak tanimlamalari
isitma.off()
sogutma.off()
sicak_led.off()
soguk_led.off()

sensor1 = ds(4)
sensor1.unit ='c'
sensor1.res = 12

sensor2 = ds(5)
sensor2.unit ='c'
sensor2.res = 12

sensor3 = ds(6)
sensor3.unit ='c'
sensor3.res = 12

sensor4 = ds(7)
sensor4.unit ='c'
sensor4.res = 12

while True:
    sicaklik_1 = ds18b20.read(sensor1)
    sicaklik_2 = ds18b20.read(sensor2)
    sicaklik_3 = ds18b20.read(sensor3)
    sicaklik_4 = ds18b20.read(sensor4)
    print(sicaklik_1, sicaklik_2, sicaklik_3, sicaklik_4)
    if (sicaklik_1 != None):
        sicaklik_1f = "%.1f" % sicaklik_1[0]
    else:
        sicaklik_1f ="N/A "
    
    if (sicaklik_2 != None):
        sicaklik_2f = "%.1f" % sicaklik_2[0]
    else:
        sicaklik_2f = "N/A "
    
    if (sicaklik_3 != None):
        sicaklik_3f = "%.1f" % sicaklik_3[0]
    else:
        sicaklik_3f ="N/A "
        
    if (sicaklik_4 != None):
        sicaklik_4f = "%.1f" % sicaklik_4[0]
    else:
        sicaklik_4f ="N/A "
        
    sicaklik_list = sicaklik_1f + sicaklik_2f + sicaklik_3f + sicaklik_4f
    uart.write(sicaklik_list)
    #yazma islemi...
    rx = bytes()
    while uart.any() > 0:
        rx += uart.read(1)
    rx = rx.decode('Ascii')
    print(rx)
    komut = rx[0:6]
    print(komut[3:6])
    if (komut == "ISA"):
        isitma.on()
    if (komut == "ISK"):
        isitma.off()
    if (komut == "STA"):
        sogutma.on()
    if (komut == "STK"):
        sogutma.off()
    if (komut[0:3] == "L1A"):
        sicak_led.on()
    if (komut[0:3] == "L1K"):
        sicak_led.off()
    if (komut[3:6] == "L2A"):
        soguk_led.on()
    if (komut[3:6] == "L2K"):
        soguk_led.off()

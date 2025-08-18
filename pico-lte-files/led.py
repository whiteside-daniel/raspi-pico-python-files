#from machine import Pin
#from utime import sleep

#led = Pin(22, Pin.OUT)

#while True:
#    led.toggle()
#    sleep(1)
    
import machine
import neopixel
import utime

NUM_LEDS = 8
pin = machine.Pin(15)
np = neopixel.NeoPixel(pin, NUM_LEDS)

# Function for rainbow effect
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            np[i] = wheel(rc_index & 255)  # Set LED color using wheel function
        np.write()
        utime.sleep_ms(wait)

def wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)  # Red to Green transition
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)  # Green to Blue transition
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)  # Blue to Red transition

sensor = machine.ADC(4)
def readTemp():
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)
i = 0
while True:
    rainbow_cycle(0)  # Call the rainbow effect function with a delay of 20 milliseconds
    if(i  == 5):
        currentTemp = readTemp()
        print(currentTemp)
        i=0
    i = i+1
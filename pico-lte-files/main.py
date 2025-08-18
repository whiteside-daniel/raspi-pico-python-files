import json
import utime as time
from pico_lte.utils.status import Status
from pico_lte.core import PicoLTE
from pico_lte.common import debug
#debug.set_level(0)
import machine
import neopixel
#CONFIGURATION
#LED config
NUM_LEDS = 8
pin = machine.Pin(15)
np = neopixel.NeoPixel(pin, NUM_LEDS)
#for datetime
rtc = machine.RTC()
datetime_now = rtc.datetime()
print(datetime_now)
#temp sensor config
sensor = machine.ADC(4)
#for LTE functionality
picoLTE = PicoLTE()
picoLTE.network.register_network()
picoLTE.http.set_context_id()
picoLTE.network.get_pdp_ready()
picoLTE.http.set_server_url()
#FUNCTIONS
#simple functions setup
def readTemp():
    #check current time
    datetime_now = rtc.datetime()
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)
# Function for rainbow effect
def rainbow_cycle(wait):
    for j in range(255):
        for i in range(NUM_LEDS):
            rc_index = (i * 256 // NUM_LEDS) + j
            np[i] = wheel(rc_index & 255)  # Set LED color using wheel function
        np.write()
        time.sleep_ms(wait)
def wheel(pos):
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)  # Red to Green transition
    elif pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)  # Green to Blue transition
    else:
        pos -= 170
        return (pos * 3, 0, 255 - pos * 3)  # Blue to Red transition
#function to POST
def postTempToAnalytics():
    debug.info("Sending a POST request.")
    print("Sending a POST request")
    #format date-time
    formattedDateTime = str(datetime_now[0]) + '-' + str(datetime_now[1]) + '-' + str(datetime_now[2]) + '-' + str(datetime_now[4])+ '-' + str(datetime_now[5])
    currentTemp = readTemp()
    payload_dict = {"date": formattedDateTime , "temp":currentTemp}
    payload_json = json.dumps(payload_dict)
    result = picoLTE.http.post(data=payload_json)
    debug.info(result)
    # Read the response after 5 seconds.
    time.sleep(5)
    result = picoLTE.http.read_response()
    if result["status"] == Status.SUCCESS:
        debug.info("Post request succeeded.")
        print("POST request succeeded")
        rainbow_cycle(5)
        rainbow_cycle(5)
        rainbow_cycle(5)
        rainbow_cycle(5)
        for i in range(NUM_LEDS):
            np[i] = (0,0,0)
        np.write()
    debug.info(result)
while True:
    postTempToAnalytics()
    time.sleep(900)
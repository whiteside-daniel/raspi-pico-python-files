import json
import time
from pico_lte.utils.status import Status
from pico_lte.core import PicoLTE
from pico_lte.common import debug
import machine
#for datetime
rtc = machine.RTC()
datetime_now = rtc.datetime()
print(datetime_now)
#temp sensor config
sensor = machine.ADC(4)
def readTemp():
    #check current time
    datetime_now = rtc.datetime()
    adc_value = sensor.read_u16()
    volt = (3.3/65535) * adc_value
    temperature = 27 - (volt - 0.706)/0.001721
    return round(temperature, 1)
currentTemp = readTemp()
#for LTE functionality
picoLTE = PicoLTE()
picoLTE.network.register_network()
picoLTE.http.set_context_id()
picoLTE.network.get_pdp_ready()
picoLTE.http.set_server_url()

debug.info("Sending a POST request.")

payload_dict = {"date": datetime_now , "temp":currentTemp}
payload_json = json.dumps(payload_dict)
result = picoLTE.http.post(data=payload_json)
debug.info(result)

# Read the response after 5 seconds.
time.sleep(5)
result = picoLTE.http.read_response()
if result["status"] == Status.SUCCESS:
    debug.info("Post request succeeded.")
debug.info(result)
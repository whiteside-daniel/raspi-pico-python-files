from machine import Pin, I2C
from utime import sleep, sleep_ms
import ssd1306
import machine
import datsunarray
datsunArray = datsunarray.datsunArray()
import wifiLogo
wifiImage = wifiLogo.wifiLogo()
import privet
privetImage = privet.privet()
import omSymbol
omImage = omSymbol.omSymbol()
import waterjug
waterImage = waterjug.waterJug()
import network
# Create I2C object
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=200000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)
display.poweron()
# Print out any addresses found
#devices = hex(i2c.scan()[0]).upper()
#print(devices)
#WIFI SETUP
ssid = 'Peaceful'
wifiPw = 'Relaxhere'
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
def connect():
    display.fill(0)
    display.text('Connecting to:',0,0,1)
    display.text(ssid,8,12,1)
    display.show()
    sleep(2)
    wlan.connect(ssid, wifiPw)
    while wlan.isconnected() == False:
        display.fill(0)
        display.text('connecting...',0,0,1)
        display.show()
        sleep(1.5)
        display.text('connecting...',8,8,1)
        display.show()
        sleep(1.5)
        display.text('connecting...',0,16,1)
        display.show()
        sleep(1.5)
        display.text('connecting...',8,24,1)
        display.show()
        sleep(1.5)
    return wlan.ifconfig()
#text logic
def newText(text, x, y, c, time):
    display.fill(0)
    display.text(text, x,y,c)
    display.show()
    sleep(time)
#render image logic
def imposeImage(dataArr,x,y):
    if(x == 'r'):
        x = 127-len(dataArr[0])
    if(y == 'b'):
        y = 31 - len(dataArr)
    elif(y == 'c'):
        y = 16 - int(len(dataArr)/2)
    for row in range(0,len(dataArr)):
        for col in range(0,len(dataArr[0])):
            display.pixel(col + x, row + y, dataArr[row][col])
    display.show()
def showWaterStatus():
    display.fill(0)
    display.show()
    imposeImage(waterImage,'r','c')
    sleep(5)
#animation logic
def slideLeft(pixelArray):
    width = len(pixelArray[1])
    xStart = 128
    yStart = 32-len(pixelArray)
    steps = 128 + width
    for i in range(0,steps):
        display.fill(0)
        for row in range(0,len(pixelArray)):
            for col in range(0,width):
                display.pixel(col + xStart, row + yStart, pixelArray[row][col])
        display.show()
        xStart = xStart - 1
def slideRight(pixelArray):
    width = len(pixelArray[1])
    xStart = width * -1
    yStart = 32-len(pixelArray)
    steps = 128 + width
    for i in range(0,steps):
        display.fill(0)
        for row in range(0,len(pixelArray)):
            for col in range(0,width):
                display.pixel(col + xStart, row + yStart, pixelArray[row][col])
        display.show()
        sleep_ms(15)
        xStart = xStart + 1
def slideDown(pixelArray):
    width = len(pixelArray[1])
    xStart = int((128-width)/2)
    yStart = 0-len(pixelArray)
    steps = 32 
    for i in range(0,steps):
        display.fill(0)
        for row in range(0,len(pixelArray)):
            for col in range(0,width):
                display.pixel(col + xStart, row + yStart, pixelArray[row][col])
        display.show()
        yStart = yStart + 1
try:
    slideDown(privetImage)
    sleep(2)
    display.fill(0)
    display.text('Welcome to',0,0,1)
    display.text('Raspberry Pi',8,8,1)
    display.show()
    sleep(2)
    connectionStats = connect()
    while True:
        display.fill(0)
        display.text('Connected on: ', 0, 0, 1)
        display.text(str(connectionStats[0]), 4,9,1)
        display.text(ssid, 4,18,1)
        imposeImage(wifiImage,'r','b')
        display.show()
        sleep(2)
        display.fill(0)
        slideLeft(datsunArray)
        slideRight(omImage)
        showWaterStatus()
except KeyboardInterrupt:
    machine.reset()



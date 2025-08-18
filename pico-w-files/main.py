#WIFI SETUP
ssid = 'ssid'
wifiPw = 'pw'
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
import namaste
namasteImage = namaste.namaste()
import network
# Create I2C object
i2c = machine.I2C(0, scl=machine.Pin(9), sda=machine.Pin(8), freq=200000)
display = ssd1306.SSD1306_I2C(128, 32, i2c)
display.poweron()
# Print out any addresses found
#devices = hex(i2c.scan()[0]).upper()
#print(devices)
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
def connect():
    wlan.connect(ssid, wifiPw)
    while wlan.isconnected() == False:
        display.fill(0)
        display.text('Connecting to:',0,0,1)
        display.text(ssid,2,8,1)
        display.show()
        sleep(.5)
        display.text('connecting...',8,16,1)
        display.show()
        sleep(.5)
        display.text('connecting...',8,24,1)
        display.show()
        sleep(.5)
    return wlan.ifconfig()
#get water level
def checkWater():
    #return a number between 0 and 100 for percentage
    return 98
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
def showWaterStatus(level):
    display.fill(0)
    display.show()
    imposeImage(waterImage,'r','c')
    display.hline(1,1,90,1)
    display.hline(1,21,90,1)
    display.vline(1,1,20,1)
    display.vline(91,1,20,1)
    display.vline(31,2,2,1)
    display.vline(61,2,2,1)
    display.vline(31,19,2,1)
    display.vline(61,19,2,1)
    display.show()
    sleep(.5)
    waterStr = 'WATER: '+str(level)+'%'
    display.text(waterStr,1,23,1)
    display.show()
    if(level > 16):
        display.fill_rect(3,3,27,17,1)
        display.show()
        sleep(.5)
        if(level > 50):
            display.fill_rect(33,3,27,17,1)
            display.show()
            sleep(.5)
            if(level > 83):
                display.fill_rect(63,3,27,17,1)
                display.show()
                sleep(.5)
    sleep(30)
#animation logic
def slideLeft(pixelArray):
    width = len(pixelArray[1])
    xStart = 128
    yStart = 32-len(pixelArray)
    xStop = -1 * width - 10
    while xStart > xStop:
        display.fill(0)
        for row in range(0,len(pixelArray)):
            for col in range(0,width):
                display.pixel(col + xStart, row + yStart, pixelArray[row][col])
        display.show()
        xStart = xStart - 4
def slideRight(pixelArray):
    width = len(pixelArray[1])
    xStart = width * -1
    yStart = 32-len(pixelArray)
    xStop = 128 + width + 10
    while xStart < xStop:
        display.fill(0)
        for row in range(0,len(pixelArray)):
            for col in range(0,width):
                display.pixel(col + xStart, row + yStart, pixelArray[row][col])
        display.show()
        sleep_ms(15)
        xStart = xStart + 2
def slideDown(pixelArray):
    height = len(pixelArray)
    width = len(pixelArray[0])
    xStart = int((128-width)/2)
    yStart = 0-len(pixelArray)
    yStop = 32 - height
    while yStart < yStop:
        display.fill(0)
        for row in range(0,height):
            for col in range(0,width):
                display.pixel(col + xStart, row + yStart, pixelArray[row][col])
        display.show()
        yStart = yStart + 2
        sleep_ms(10)
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
        waterLevel = checkWater()
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
        slideLeft(namasteImage)
        showWaterStatus(waterLevel)
except KeyboardInterrupt:
    machine.reset()

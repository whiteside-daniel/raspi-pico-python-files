import machine
#for datetime
rtc = machine.RTC()
datetime_now = rtc.datetime()
print(datetime_now)
formattedDateTime = str(datetime_now[0]) + '-' + str(datetime_now[1]) + '-' + str(datetime_now[2]) + '-' + str(datetime_now[4])+ '-' + str(datetime_now[5])
print(formattedDateTime)
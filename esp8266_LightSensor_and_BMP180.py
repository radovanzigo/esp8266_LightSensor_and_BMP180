########################
#                      #
# 2020-05-10 by Zigi   #
########################

sleep_wifi_init=5
sleep_main_cycle=30

import network
import time

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect("Wifi_user", "Wifi_passwd")
    time.sleep(sleep_wifi_init) # waiting for wifi
    while not sta_if.isconnected():
        pass
print(sta_if.ifconfig())



import machine
import bmp180

led = machine.Pin(2, machine.Pin.OUT)

# Light sensor
from machine import ADC

# BMP180
from bmp180 import BMP180
from machine import I2C, Pin
bus =  I2C(scl=Pin(5), sda=Pin(4), freq=100000)

# configure RTC.ALARM0 to be able to wake the device
rtc = machine.RTC()
rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

# set RTC.ALARM0 to fire after 10 seconds (waking the device)
rtc.alarm(rtc.ALARM0, 30000)


try:

    adc = ADC(0)
    bmp180 = BMP180(bus)
    bmp180.oversample_sett = 3
    bmp180.baseline = 101325
    

except:

    print ("Initial sensor timeout, continuing..") 

import urequests
import ubinascii

user_and_pass = str(ubinascii.b2a_base64("%s:%s" % ("InfluxDB_user", "InfluxDB_passwd"))[:-1], 'utf-8')
headers = {'Authorization': 'Basic %s' % user_and_pass}
#print (headers)


MIN_VALUE=0
MAX_VALUE=1024

while True:

    try:

      led.value(0)  # LED ON
      LightSensorValue = adc.read()
      
      esp8266_light = 100 - ((LightSensorValue - MIN_VALUE) * 100 / (MAX_VALUE - MIN_VALUE));
    
      temp = bmp180.temperature - 8.9   # 8.9 is defauelt error of my sensor :)
      print("reading pressure")
      # WarmUP sensor to have better measurement quality
      presure = bmp180.pressure / 100
      time.sleep(2)
      presure = bmp180.pressure / 100
      time.sleep(2)
      presure = bmp180.pressure / 100
      time.sleep(2)
      presure = bmp180.pressure / 100
      time.sleep(2)
      presure = bmp180.pressure / 100
      time.sleep(2)
      presure = bmp180.pressure / 100
      print("reading pressure - done")
      altitude = bmp180.altitude

    except:

      print("Sensor timeout, retrying..")
      print("Giong to sleep")
      machine.deepsleep()

      continue


    url_string = 'https://domain.com/write?db=DB_name'
    data_string = 'metric=esp8266_light,host=sensor2 value=%s' % (esp8266_light)
    data_string = '%s\nmetric=esp8266_temp,host=sensor2 value=%s' % (data_string, temp)
    data_string = '%s\nmetric=esp8266_presure,host=sensor2 value=%s' % (data_string, presure)
    data_string = '%s\nmetric=esp8266_altitude,host=sensor2 value=%s' % (data_string, altitude)

    print(data_string)

    try:

      r = urequests.post(url_string, data=data_string, headers=headers)
      r.close()

    except:

      print("Unable to submit data to server")

    led.value(1)  # LED OFF
    print("Giong to sleep")
    machine.deepsleep()

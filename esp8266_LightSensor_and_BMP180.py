########################
#                      #
# 2020-05-06 by Zigi   #
########################

sleep_wifi_init=5
sleep_main_cycle=10

import network
import time

sta_if = network.WLAN(network.STA_IF)
if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect("Wifi", "Passwd")
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



try:

    adc = ADC(0)
    bmp180 = BMP180(bus)
    bmp180.oversample_sett = 3
    bmp180.baseline = 101325
    

except:

    print ("Initial sensor timeout, continuing..") 

import urequests
import ubinascii

user_and_pass = str(ubinascii.b2a_base64("%s:%s" % ("InfluxDB_User", "InfluxDB_Passwd"))[:-1], 'utf-8')
headers = {'Authorization': 'Basic %s' % user_and_pass}
#print (headers)


MIN_VALUE=0
MAX_VALUE=1024

while True:

    try:

      led.value(0)  # LED ON
      LightSensorValue = adc.read()
      
      esp8266_light = 100 - ((LightSensorValue - MIN_VALUE) * 100 / (MAX_VALUE - MIN_VALUE));
#      esp8266_light = 1024 - LightSensorValue
    
      temp = bmp180.temperature
      presure = bmp180.pressure / 100
      altitude = bmp180.altitude

    except:

      print("Sensor timeout, retrying..")

      time.sleep(sleep_main_cycle)

      continue


    url_string = 'https://aaa.com/write?db=DBname'
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
    time.sleep(sleep_main_cycle)

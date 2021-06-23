# esp8266_LightSensor_and_BMP180
D1 Mini Pro  esp8266_LightSensor_and_BMP180

Used Library:
https://github.com/micropython-IMU/micropython-bmp180

Used rezistor 100K

![alt text](https://github.com/radovanzigo/esp8266_LightSensor_and_BMP180/blob/master/D1miniPro_LightSensor_BMP180.jpg?raw=true)


Flashing ESP for uPython

## Check ROM size
esptool.py --port COM4 flash_id

## Erase flash
esptool.py --port COM4 erase_flash

## Flash ... example is for D1 Mini Pro ... flash_size 16MB not working !!!
esptool.py --port COM4 --baud 115200 write_flash --flash_size=4MB --flash_mode qio 0x00000 C:\path\esp8266-20191220-v1.12.bin

Do not use Daily builds ... isuue with urequests

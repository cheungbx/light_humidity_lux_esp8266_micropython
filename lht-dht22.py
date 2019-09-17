# ESP8266 iot humdity temperature sensor with LED switch and pump switch , MQTT and  NTP time.
# GPIO4 aka D2 for SDA of I2C OLED SSD1306 
# GPIO5 aka D1 for SCL of I2C OLED SSD1306 


# led  D6  GPIO 12
# pump D5  GPIO 14
# btn1 D4  GPIO 2
# btn2 D3  GPIO 0

import machine
import network
import time
import dht
from time import sleep
from machine import Pin, I2C
from dht import DHT11

import os
import sys
import ssd1306

  

def fill_zero(n):   
    if n < 10:   
        return '0' + str(n) 
    else:   
        return str(n) 

def fill_blank(n):     
    if n<10:
        return ' ' + str(n)
    else:
        return str(n)
 


i2c = I2C(-1, Pin(5), Pin(4))   # SCL, SDA
display = ssd1306.SSD1306_I2C(128, 64, i2c)
        
# WiFi connection information
WIFI_SSID = 'BILLYWIFI'
WIFI_PASSWORD = 'Xolmem13'

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()

# set time using NTP server on the internet

import ntptime    #NTP-time (from pool.ntp.org) 
import utime
ntptime.settime()
tm = utime.localtime(utime.mktime(utime.localtime()) + 8 * 3600)
tm=tm[0:3] + (0,) + tm[3:6] + (0,)
rtc = machine.RTC()
rtc.datetime(tm)
 

reported_err = 0
measure_period_ms = 10000
display_period_ms = 1000
loop_delay_ms = 10
last_measure_ms = 0
last_display_ms = 0
debounce_start_ms = 0
debounce_period_ms = 20
last_btn1_state = 0
last_btn2_state = 0
btn1_state = 0
btn2_state = 0
ledOn = False
pumpOn = False
h = 72.5
h0 = 1.0
t = 28.3
t0 = 1.0

led = Pin(12, Pin.OUT) 
pump = Pin(14, Pin.OUT)
btn1 = Pin(2, Pin.IN, Pin.PULL_UP)
btn2 = Pin(0, Pin.IN, Pin.PULL_UP)


# pin for DHT sensor
dhtSensor = DHT11(Pin(13, Pin.IN, Pin.PULL_UP))



while True:

    # led switch
    btn1_value = btn1.value()
    if btn1_value != last_btn1_state :
        debounce_start_ms = time.ticks_ms()
    if abs(time.ticks_ms() - debounce_start_ms) >= debounce_period_ms :
        if btn1_value != btn1_state :
            btn1_state = btn1_value
            if btn1_state == 1 :
                if ledOn :
# if led is previously ON, now turn it off by outputing High voltage
                    led.on()
                    msg = "OFF"
                    ledOn = False
                else :
# if led is previously OFF, now turn it on by outputing Low voltage
                    led.off()
                    msg = "ON"
                    ledOn = True

 
    last_btn1_state = btn1_value


    # pump switch
    btn2_value = btn2.value()
    if btn2_value != last_btn2_state :
        debounce_start_ms = time.ticks_ms()
    if abs(time.ticks_ms() - debounce_start_ms) >= debounce_period_ms :
        if btn2_value != btn2_state :
            btn2_state = btn2_value
            if btn2_state == 1 :
                if pumpOn :
# if pump is previously ON, now turn it off by outputing High voltage
                    pump.on()
                    msg = "OFF"
                    pumpOn = False
                else :
# if pump is previously OFF, now turn it on by outputing Low voltage
                    pump.off()
                    msg = "ON"
                    pumpOn = True

    last_btn2_state = btn2_value

    # Sensors
    try:
        if abs(time.ticks_ms() - last_measure_ms) >= measure_period_ms :
            try:
                dhtSensor.measure()   # Poll sensor
                h = dhtSensor.humidity()
                t = dhtSensor.temperature()
            except OSError as err :
                print("dhtSensor error: {0}".format(err))
            msg = (b'{0:3.1f}'.format(h))
            if h != h0 :
                print('Publish:  humidity = {}'.format(h))
                h0 = h

            msg = (b'{0:3.1f}'.format(t))
            if t != t0 :
                print('Publish:  airtemp = {}'.format(t))
                t0 = t
                
            last_measure_ms = time.ticks_ms()

        if abs(time.ticks_ms() - last_display_ms) >= display_period_ms :
            display.fill(0)
            Y,M,D,H,m,S,ms,W=utime.localtime()
            timetext ='%s-%s %s:%s:%s' % (fill_zero(M),fill_zero(D),fill_zero(H),fill_zero(m),fill_zero(S))       
            display.text(timetext,0,0)
            display.text(b'{0:3.1f} %'.format(h), 0, 24)
            display.text(b'{0:3.1f} C'.format(t), 64, 24)  
            if ledOn :
                display.text("LED ON", 0, 48)
            else :
                display.text("LED OFF", 0, 48)
                             
            if pumpOn :
                display.text("PUMP ON", 64, 48)
            else :
                display.text("PUMP OFF", 64, 48)

            display.show()  
            last_display_ms = time.ticks_ms()
            
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        sys.exit()
    

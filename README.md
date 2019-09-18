# light_humidity_lux_esp8266_micropython
# Light Humidity Lux sensor plus IoT controlled LED on ESP8266 Node MCU D1 Mini for both I2C SSD1306 and SPI SSD1306 display
# ESP8266 iot humdity temperature sensor with LED switch and pump switch , MQTT and  NTP time.
# press LEFT button to exit the program.
# press A to turn the LED on or off
# ----------------------------------------------------------
#lht.py - i2C version for ssd1306 display, and i2c interface with SHT20 humidity and temperature sensor and BH1750fvi light meter sensor 
#
#lhts.py - SPI version for ssd1306 display,and i2c interface with SHT20 humidity and temperature sensor and BH1750fvi light meter sensor  
#lhts.mpy - precompiled byte code version of lhts.py
#lht-DHT11.py - i2C version for ssd1306 display, and one wire interface with DHT-11 humidity and temperature sensor
#
# Pins used for SPI version
# ESP8266 (node MCU D1 mini)  micropython
# by Billy Cheung  2019 08 31
#
# SPI OLED
# GND
# VCC
# D0/Sck - D5 (=GPIO14=HSCLK)
# D1/MOSI- D7 (=GPIO13=HMOSI)
# RES    - D0 (=GPIO16)
# DC     - D4 (=GPIO2)
# CS     - D3 (=GPIO0)
# 
# GPIO15   D8  LED  / Speaker
# n.c.   - D6  (=GPIO13=HMOSI)
#
# GPIO5    D1——   On to read ADC for Btn / SCL for i2c sensors
# GPIO4    D2——   On to read ADC for Paddle / SDA for i2c sensors
#
# buttons   A0
# A0 VCC-9K-U-9K-L-12K-R-9K-D-9K-A-12K-B-9K-GND
#
# Pins used for I2C vesion
#------------------------------------
# GPIO4 aka D2 for SDA of I2C OLED SSD1306 
# GPIO5 aka D1 for SCL of I2C OLED SSD1306 
# Btn1Pin  12    // D6 - button 1 for LED 
# DHTPIN   13    // D7 data pin for the humidity sensor (not required if SHT20 is used)
# LedPin   14    // D5   LED output pin 
# Btn2Pin  2     // D4 - button 2 for pump
# PumpPin  0     // D3 - Pump output pin

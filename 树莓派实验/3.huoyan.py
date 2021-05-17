#!/usr/bin/python
# encoding:utf-8
import RPi.GPIO as GPIO
import time

# 火焰传感器引脚
pin_fire = 25
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin_fire, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
try:
    while True:
        status = GPIO.input(pin_fire)
        if status == True:
            print('没有检测到火灾')
        else:
            print('检测到火灾')
        time.sleep(0.5)
except KeyboardInterrupt:
    GPIO.cleanup()

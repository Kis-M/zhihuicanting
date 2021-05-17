#!/usr/bin/env python
import RPi.GPIO as GPIO

Buzzer = 24  # pin11
GPIO.setwarnings(False)

GPIO.setmode(GPIO.BCM)  # Numbers GPIOs by physical location
GPIO.setup(Buzzer, GPIO.OUT)
GPIO.output(Buzzer, GPIO.HIGH)


def on():
    GPIO.output(Buzzer, GPIO.LOW)


def off():
    GPIO.output(Buzzer, GPIO.HIGH)


if __name__ == '__main__':  # Program start from here
    off()

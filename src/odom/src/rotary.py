#!/usr/bin/env python
import RPi.GPIO as GPIO

class Rotary():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(15,GPIO.IN)
        GPIO.setup(18,GPIO.IN)

        self.count = 0

    def event(self):
        GPIO.add_event_detect(15,GPIO.RISING, callback=self.handle_pulse_event)
	print ("C1 =" + str(GPIO.input(15)))
	print ("C2 =" + str(GPIO.input(18)))

    def handle_pulse_event(self):
	print ("IN")
        if GPIO.input(18):
            self.count -= 1
        else:
            self.count += 1

if __name__ == "__main__":
    clas = Rotary()
    clas.event()


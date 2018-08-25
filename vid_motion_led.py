#!/usr/bin/env python
# python3

import time
import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO
from gpiozero import LED

#camera settings:
camera = PiCamera()
camera.rotation = 180
camera.led = False
camera.framerate = 25

save_dir = "/home/pi/vid/"

#motion settings:
GPIO.setmode(GPIO.BCM)
GPIO_PIR = 17
led = LED(4)

# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)
#GPIO.setup(4,GPIO.OUT)
#GPIO.output(4,GPIO.LOW)

#VIDEO -------------------------------------------------
def video_rec():
    camera.resolution = (1296, 972)
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start = datetime.datetime.now()
    def get_file_name():
        return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
    filename = "%s%s" % (save_dir, get_file_name())
    camera.start_preview()
    camera.start_recording(filename)
    while (datetime.datetime.now() - start).seconds < 60:
        camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(0.2)
    camera.stop_recording()
    camera.stop_preview()
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #print("Finished recording @ %s" % (time_now))

#TAKES 2 STILL PICTURES -------------------------------------------------
def still():
    camera.exposure_mode = 'night'
    camera.awb_mode = 'shade'
    camera.resolution = (2592, 1944)
    camera.rotation = 180
    camera.led = False
    camera.start_preview()
    time.sleep(0.2)
    def get_file_name():
    	return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Taking picture at %s" % (time_now))
    filename = "%s%s" % (save_dir, get_file_name())
    camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.capture(filename)
    time.sleep(0.2)
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    camera.capture(filename)
    camera.stop_preview()

#PIR ---------------------------------------------------
print("PIR Module Holding Time Test (CTRL-C to exit)")

Current_State  = 0
Previous_State = 0

try:

    print("Waiting for PIR to settle ...")
    # Loop until PIR output is 0
    while GPIO.input(GPIO_PIR)==1:
        Current_State  = 0
    print("  Ready")
    # Loop until users quits with CTRL-C
    while True :
    # Read PIR state
        Current_State = GPIO.input(GPIO_PIR)
        timestamp = datetime.datetime.now().time()
        start = datetime.time(6, 31)
        end = datetime.time(19, 0)
        midnight = datetime.time(23, 59)
        if (Current_State==1 and Previous_State==0) and (start <= timestamp <= end):
    # PIR is triggered
        #start_time=time.time()
            time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("  Motion detected @ %s !" % time_now)
            #GPIO.output(4,GPIO.HIGH)
            led.blink()
            video_rec()
            led.off()
            #GPIO.output(4,GPIO.LOW)
        elif (Current_State==1 and Previous_State==0) and (end < timestamp <= midnight):
    # PIR is triggered
            time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("  Motion detected @ %s !" % time_now)
            led.blink()
            #GPIO.output(4,GPIO.HIGH)
            still()
            led.off()
            #GPIO.output(4,GPIO.LOW)
        elif (Current_State==1 and Previous_State==0) and (timestamp < start):
            # PIR is triggered
            time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            print("  Motion detected @ %s !" % time_now)
            led.blink()
            #GPIO.output(4,GPIO.HIGH)
            still()
            led.off()
            #GPIO.output(4,GPIO.LOW)
            # Record previous state
            Previous_State=1
        elif Current_State==0 and Previous_State==1:
        	# PIR has returned to ready state
        	stop_time=time.time()
        	print("  Ready ")
            #led.off()
            #GPIO.output(4,GPIO.LOW)
        	Previous_State=0
except KeyboardInterrupt:
    print("  Quit")
    #GPIO.output(4,GPIO.LOW)
    led.off()
    #Reset GPIO settings
    GPIO.cleanup()

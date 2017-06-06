#!/usr/bin/env python
#python2

import time
import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO
#import os

#camera settings:
camera = PiCamera()
camera.rotation = 180
camera.led = False
camera.framerate = 25
camera.resolution = (960, 540)
save_dir = "/home/pi/vid/"

#motion settings:
GPIO_PIR = 17
GPIO.setmode(GPIO.BCM)

#VIDEO -------------------------------------------------
def video_rec():
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    start = datetime.datetime.now()
    def get_file_name():
        return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
    filename = "%s%s" % (save_dir, get_file_name())
    #print("*** OG is out, starting to record at %s ***" % (time_now))
    camera.start_preview()
    camera.start_recording(filename)
    while (datetime.datetime.now() - start).seconds < 60:
        camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        camera.wait_recording(0.2)
    camera.stop_recording()
    camera.stop_preview()
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Finished recording @ %s" % (time_now))

#TAKES 2 STILL PICTURES -------------------------------------------------
def still():
	camera.exposure = night
	camera.resolution = (2592, 1944)
	camera.rotation = 180
	camera.led = False
	camera.start_preview()
	time.sleep(2)
	def get_file_name():
		return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
	time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	print("Taking picture at %s" % (time_now))
	filename = "%s%s" % (save_dir, get_file_name())
	camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	camera.capture(filename)
	time.sleep(1)
	time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	camera.capture(filename)
	camera.stop_preview()

#PIR ---------------------------------------------------
print("PIR Module Holding Time Test (CTRL-C to exit)")
# Set pin as input
GPIO.setup(GPIO_PIR,GPIO.IN)

Current_State  = 0
Previous_State = 0

try:

  print "Waiting for PIR to settle ..."
  # Loop until PIR output is 0
  while GPIO.input(GPIO_PIR)==1:
    Current_State  = 0
  print "  Ready"
  # Loop until users quits with CTRL-C
  while True :
    # Read PIR state
    Current_State = GPIO.input(GPIO_PIR)
    timestamp = datetime.datetime.now().time()
    start = datetime.time(6, 31)
    end = datetime.time(19, 0)
    midnight = datetime.time(23, 59)
    if (Current_State==1 and Previous_State==0) and (start < timestamp < end):
    # PIR is triggered
        #start_time=time.time()
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "  Motion detected @ %s !" % time_now
        video_rec()
    elif (Current_State==1 and Previous_State==0) and (end < timestamp <= midnight):
    # PIR is triggered
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "  Motion detected @ %s !" % time_now
        still()
    elif (Current_State==1 and Previous_State==0) and (timestamp < start):
    # PIR is triggered
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print "  Motion detected @ %s !" % time_now
        still()

    # Record previous state
	Previous_State=1
    elif Current_State==0 and Previous_State==1:
    	# PIR has returned to ready state
    	stop_time=time.time()
    	print "  Ready "
    	Previous_State=0

except KeyboardInterrupt:
  print "  Quit"
  # Reset GPIO settings
  GPIO.cleanup()

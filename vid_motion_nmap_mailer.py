#!/usr/bin/env python
#python 3

import time
import datetime
from picamera import PiCamera
import RPi.GPIO as GPIO
import nmap
import smtplib
#import os

#camera settings:
camera = PiCamera()
nm = nmap.PortScanner()

camera.rotation = 180
camera.led = False
camera.framerate = 25

save_dir = "/home/pi/vid/"

time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print(('Scan started at %s ') % time_now)

#EMAIL -------------------------------------------------
def email():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("username", "passwrd")
    msg = "Motion detected!"
    server.sendmail("username", "recipients_email", msg)
    server.quit()

#VIDEO -------------------------------------------------
def video_rec():
    #camera.resolution = (960, 540)
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

#NMAP SCANNER:
#def sweep():
while True:
        #motion settings:
        count=0
        print('----------------------------------------------------')
        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        nm.scan(hosts='10.0.0.16', arguments='-sn')
        #print(('Scan started at %s ') % time_now)
        for host in nm.all_hosts():
                #print('Host : %s (%s)' % (host, nm[host].hostname()))
                #print('State : %s' % nm[host].state())
                if nm[host].state()=='up':
                        count+=1
                        #print('OG is in, counted up by 1')
        if count > 0:
                #print('OG is in. Scanning again in 5 minutes')
                time.sleep(300)
        else:
                time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print('OG is out @ %s' % (time_now))
                time.sleep(1)
                #print("PIR Module Holding Time Test (CTRL-C to exit)")
                # Set pin as input
                GPIO_PIR = 17
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(GPIO_PIR,GPIO.IN)

                Current_State  = 0
                Previous_State = 0

                try:
                  #print("Waiting for PIR to settle ...")
                  # Loop until PIR output is 0
                  while GPIO.input(GPIO_PIR)==1:
                    Current_State  = 0
                  #print("PIR Active")
                  # Loop until users quits with CTRL-C
                  t_end = time.time() + 300

                  while time.time() < t_end :
                    # Read PIR state
                    Current_State = GPIO.input(GPIO_PIR)
                    timestamp = datetime.datetime.now().time()
                    start = datetime.time(6, 31)
                    end = datetime.time(20, 30)
                    midnight = datetime.time(23, 59)
                    if (Current_State==1 and Previous_State==0) and (start <= timestamp <= end):
                    # PIR is triggered
                        #start_time=time.time()
                        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print("  Motion detected @ %s !" % time_now)
                        video_rec()
                    elif (Current_State==1 and Previous_State==0) and (end < timestamp <= midnight):
                    # PIR is triggered
                        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print("  Email sent: Motion detected @ %s !" % time_now)
                        email()
                    elif (Current_State==1 and Previous_State==0) and (timestamp < start):
                    # PIR is triggered
                        time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        print("  Email sent: Motion detected @ %s !" % time_now)
                        email()
                    # Record previous state
                        Previous_State=1
                    elif Current_State==0 and Previous_State==1:
                    	# PIR has returned to ready state
                    	stop_time=time.time()
                    	print("  At the end, Ready ")
                    	Previous_State=0

                except KeyboardInterrupt:
                  print("  Quit")
                  # Reset GPIO settings
                  GPIO.cleanup()

#for i in range(36): #loop for 1 hour
#        sweep()
#        time.sleep(1)

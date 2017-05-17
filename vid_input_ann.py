#!/usr/bin/env python

from picamera import PiCamera
import time
import datetime

camera = PiCamera()
camera.rotation = 180
camera.led = False
camera.framerate = 25
camera.resolution = (960, 540)
save_dir = "/home/pi/vid/"

hours = int(input("How many hours would you like to record? "))
time.sleep(1)
chunk_size = int(input("How many minutes do you want each clip to be? "))
chunk_size_secs = chunk_size*60
chunk_per_hour = 60/chunk_size
repeat_code = int(chunk_per_hour*hours)
print("%s hours recording starting now" % hours)

def repeat():
	start = datetime.datetime.now()
	def get_file_name():
	 return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
	time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	filename = "%s%s" % (save_dir, get_file_name())
	time.sleep(1)
	print("Starting to record a %s minute chunk at %s" % (chunk_size, time_now))

	camera.start_preview()
	camera.start_recording(filename)

	while (datetime.datetime.now() - start).seconds < chunk_size_secs:
	    camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	    camera.wait_recording(0.2)
	camera.stop_recording()
	camera.stop_preview()

for i in range(repeat_code):
	repeat()

print("Finished recording")

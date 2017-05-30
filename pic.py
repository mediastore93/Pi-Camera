from time import sleep
from picamera import PiCamera
import time
import datetime

camera = PiCamera()
camera.resolution = (1920, 1080)
camera.rotation = 180
#camera.led = False
save_dir = "/home/pi/vid/"
#time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'

camera.start_preview()
sleep(2)
def get_file_name():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.jpg")
time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("Taking picture at %s" % (time_now))
filename = "%s%s" % (save_dir, get_file_name())
camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
camera.capture('filename')
camera.stop_preview()

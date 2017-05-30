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

def get_file_name():
	return datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
filename = "%s%s" % (save_dir, get_file_name()) 
print('taking picture')
camera.start_preview()
sleep(2)
camera.annotate_text = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
camera.capture('filename.jpg')
camera.stop_preview()

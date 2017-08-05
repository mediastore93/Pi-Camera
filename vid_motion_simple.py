from gpiozero import MotionSensor
from picamera import PiCamera
from datetime import datetime

camera = PiCamera()
pir = MotionSensor(17)

camera.rotation = 180
camera.framerate = 30
camera.resolution = (1296, 972)
save_dir = "/home/pi/vid/"

while True:
    pir.wait_for_motion()
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    filename = datetime.now().strftime("%Y-%m-%d_%H.%M.%S.h264")
    camera.start_recording(filename)
    print("Motion detected, started recording @ %s" % (time_now))
    camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    pir.wait_for_no_motion()
    camera.stop_recording()
    time_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("Stopped recording @ %s" % (time_now))

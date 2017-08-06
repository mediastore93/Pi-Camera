from gpiozero import MotionSensor
from datetime import datetime

camera = PiCamera()
pir = MotionSensor(17)

while True:
    time_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print("PIR started @ %s" % (time_now))
    pir.wait_for_motion()  
    print("Motion detected @ %s" % (time_now))
    pir.wait_for_no_motion()

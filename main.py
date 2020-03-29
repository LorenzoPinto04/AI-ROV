from sense_hat import SenseHat
import numpy as np
import cv2
import numpy as np
from imutils.video import VideoStream
import time

vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)

sense = SenseHat()
sense.clear()

auto = False
manual = True



red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# examples using (x, y, pixel)

motor_front_dx = ((2,0),(1,1), (2,1), (1,0))
motor_front_sx = ((2,7),(1,7), (2,6), (1,6))
motor_back_dx = ((7,0),(7,1), (6,0), (6,1))
motor_back_sx = ((7,7),(6,6), (6,7), (7,6))
motor_vert = ((3,3),(4,4), (3,4), (4,3))

def motor_react(motor, color):
    for i in motor:
        sense.set_pixel(i[0], i[1], color)
        
if auto:
    yaw_abs = sense.get_accelerometer()['yaw']
    press_abs = sense.get_pressure()

while True:
    frame = vs.read()
    cv2.imshow("ROV", frame)
    # The event listener will be running in this block
    gyro = sense.get_gyroscope()
    press = sense.get_pressure()
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    if auto:
        if 0 < gyro['yaw'] < 180:
            motor_react(motor_back_dx, green)
            motor_react(motor_back_sx, red)
        elif 180 < gyro['yaw'] < 360:
            motor_react(motor_back_sx, green)
            motor_react(motor_back_dx, red)
        if press > press_abs:
            motor_react(motor_vert, green)
        elif press < press_abs:
            motor_react(motor_vert, red)
    if manual:
        if key == ord('e'):
            print('forward')
            motor_react(motor_back_dx, green)
            motor_react(motor_back_sx, green)
        if key == ord('d'):
            print('backward')
            motor_react(motor_back_dx, red)
            motor_react(motor_back_sx, red)
        pass
    #pygame.display.flip()
        
    
    

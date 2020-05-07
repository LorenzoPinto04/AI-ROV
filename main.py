import functions as f
# if you are executing the code from your raspberry with a cam module and a SenseHat connected set simulation = False, otherwise use the simulation mode
simulation_mode = True

from imutils.video import VideoStream
import numpy as np
import cv2
import numpy as np
import time
import pygame
if not simulation_mode:
    from sense_hat import SenseHat
else:
    from sense_emu import SenseHat
    
sense = SenseHat()
sense.clear()

vs = VideoStream(usePiCamera = not simulation_mode).start()
time.sleep(1.0)

cv2.namedWindow("ROV", cv2.WINDOW_NORMAL)       
cv2.resizeWindow('ROV', 600,600)
pygame.init()  




auto = False
use_keyboard = True
use_controller = False



red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
off = (0, 0, 0)

motor_front_dx = ((2,0),(1,1), (2,1), (1,0))
motor_front_sx = ((2,7),(1,7), (2,6), (1,6))
motor_back_dx = ((7,0),(7,1), (6,0), (6,1))
motor_back_sx = ((7,7),(6,6), (6,7), (7,6))
motor_vert = ((3,3),(4,4), (3,4), (4,3))
front_lights = ((0,1),(0,6))

    
telemetry_dict = {'light' : 'OFF'}        
        
if auto:
    yaw_abs = sense.get_accelerometer()['yaw']
    press_abs = sense.get_pressure()
dict_sensors = 0

direction = ''


while True:
    telemetry_dict['direction'] = direction
    frame = vs.read()
    dict_sensors = f.get_dict_sensors(sense, telemetry_dict)
    f.display_telemetry(frame, dict_sensors)
    cv2.imshow("ROV", frame)
    direction = ''
    key = cv2.waitKey(1) & 0xFF
    if auto:
        if 0 < gyro['yaw'] < 180:
            f.motor_react(motor_back_dx, green)
            f.motor_react(motor_back_sx, red)
        elif 180 < gyro['yaw'] < 360:
            f.motor_react(motor_back_sx, green)
            f.motor_react(motor_back_dx, red)
        if press > press_abs:
            f.motor_react(motor_vert, green)
        elif press < press_abs:
            f.motor_react(motor_vert, red)
    if use_keyboard:
        if key == 27:
            print('[INFO] Programma interrotto')
            break
        if key == 32:
            print('[INFO] Pause')
            cv2.waitKey(0)

        # MOVEMENTS 
        # right pad
        if key == ord('e'):
            direction = 'forward'
        if key == ord('d'):
            direction = 'backward'
        if key == ord('f'):
            direction = 'right'
        if key == ord('s'):
            direction = 'left'
        # left  pad
        if key == 112:
            direction = 'up'
        if key == 210:
            direction = 'down'
        if key == ord('l'):
            direction = 'shift_left'
        if key == 192:
            direction = 'shift_right'
        if key == ord('k'):
            direction = 'roll_left'
        if key == 217:
            direction = 'roll_right'
        # LIGHTS
        if key == ord('n'):
            dict_sensors['light'] = 'ON'
            f.lights(True)
        if key == ord('m'):
            dict_sensors['light'] = 'OFF'
            f.lights(False)


cv2.destroyAllWindows()
        

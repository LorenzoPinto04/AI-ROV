# if you are executing the code from your raspberry with a cam module and a SenseHat connected set simulation = False, otherwise use the simulation mode
simulation_mode = True

from imutils.video import VideoStream
import numpy as np
import cv2
import numpy as np
import time
from math import cos, sin, tan, pi, radians
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


# examples using (x, y, pixel)

motor_front_dx = ((2,0),(1,1), (2,1), (1,0))
motor_front_sx = ((2,7),(1,7), (2,6), (1,6))
motor_back_dx = ((7,0),(7,1), (6,0), (6,1))
motor_back_sx = ((7,7),(6,6), (6,7), (7,6))
motor_vert = ((3,3),(4,4), (3,4), (4,3))
front_lights = ((0,1),(0,6))

def motor_react(motor, color):
    for i in motor:
        sense.set_pixel(i[0], i[1], color)
    return


def lights(status):
    if status:
        motor_react(front_lights, white)
        return
    motor_react(front_lights, off)

def write_on_screen(image, text, value, position):
    cv2.putText(image,text.format(value), position, cv2.FONT_HERSHEY_SIMPLEX, .3, 255)

    


def sketch_horizon_line(image, degree, xcenter, ycenter):
    lenght = 80
    degree = degree -180
    theta_rad = pi/2 - radians(degree)
    ynew = int(xcenter + lenght*cos(theta_rad))
    xnew = int(ycenter + lenght*sin(theta_rad))
    cv2.line(image,(xcenter,ycenter),(xnew,ynew),(255,0,0),1)
    degree = degree + 180
    theta_rad = pi/2 - radians(degree)
    ynew = int(xcenter + lenght*cos(theta_rad))
    xnew = int(ycenter + lenght*sin(theta_rad))
    cv2.line(image,(xcenter,ycenter),(xnew,ynew),(255,0,0),1)


def display_telemetry(image, dict_sensors):
    write_on_screen(image, "Pressure: {0:.1f}", dict_sensors['pressure'], (10,10))
    write_on_screen(image, "Temperature: {0:.1f}", dict_sensors['temperature'], (10,20))
    write_on_screen(image, "Humidity: {0:.1f}%", dict_sensors['humidity'], (10,30))
    write_on_screen(image, "Light: {}", dict_sensors['light'], (10,40))
    write_on_screen(image, "{}", dict_sensors['direction'], (140,220))
    write_on_screen(image, "Roll: {0:.0f}", dict_sensors['orientation']['roll'], (10,50))
    write_on_screen(image, "Pitch: {0:.0f}", dict_sensors['orientation']['pitch'], (10,60))
    write_on_screen(image, "Yaw: {0:.0f}", dict_sensors['orientation']['yaw'], (10,70))
    #write_on_screen(image, "North: {0:.0f}", dict_sensors['compass_north'], (10,80))
    roll_angle = dict_sensors['orientation']['roll']
    sketch_horizon_line(image, roll_angle, 150, 150)
    return


    
def get_dict_sensors(sense, values):
    #values['gyro'] = sense.get_gyroscope()
    values['pressure'] = sense.get_pressure()
    values['temperature'] = sense.get_temperature()
    values['humidity'] = sense.get_humidity()
    values['orientation'] = sense.get_orientation()
    #values['compass_north'] = north = sense.get_compass()
    return values
    
telemetry_dict = {'light' : 'OFF'}        
        
if auto:
    yaw_abs = sense.get_accelerometer()['yaw']
    press_abs = sense.get_pressure()
dict_sensors = 0

direction = ''

a = 0

while True:
    a += 1
    telemetry_dict['direction'] = direction
    frame = vs.read()
    dict_sensors = get_dict_sensors(sense, telemetry_dict)
    display_telemetry(frame, dict_sensors)
    cv2.imshow("ROV", frame)
    direction = ''
    key = cv2.waitKey(1) & 0xFF
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
            lights(True)
        if key == ord('m'):
            dict_sensors['light'] = 'OFF'
            lights(False)


cv2.destroyAllWindows()
        

from sense_hat import SenseHat
import numpy as np
import cv2
import numpy as np
from imutils.video import VideoStream
import time
from math import cos, sin, tan, pi, radians

vs = VideoStream(usePiCamera=True).start()
time.sleep(2.0)
cv2.namedWindow("ROV", cv2.WINDOW_NORMAL)       
cv2.resizeWindow('ROV', 600,600)


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
        return

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

def point_pos(x0, y0, d, theta):
    theta_rad = pi/2 - radians(theta)
    return x0 + d*cos(theta_rad), y0 + d*sin(theta_rad)


def display_telemetry(image, dict_sensors):
    cv2.putText(image,"Pressure: {0:.1f}".format(dict_sensors['pressure']), (10,10), cv2.FONT_HERSHEY_SIMPLEX, .3, 255)
    cv2.putText(image,"Temperature: {0:.1f}".format(dict_sensors['temperature']), (10,20), cv2.FONT_HERSHEY_SIMPLEX, .3, 255)
    cv2.putText(image,"Humidity: {0:.1f}%".format(dict_sensors['humidity']), (10,30), cv2.FONT_HERSHEY_SIMPLEX, .3, 255)
    cv2.putText(image,"Light: {}".format(dict_sensors['light']), (10,40), cv2.FONT_HERSHEY_SIMPLEX, .3, 255)
    cv2.putText(image, dict_sensors['direction'], (140,220), cv2.FONT_HERSHEY_SIMPLEX, .3, 255)
    cv2.putText(image,"Roll: {0:.0f}".format(dict_sensors['orientation']['roll']), (10,50), cv2.FONT_HERSHEY_SIMPLEX, .3, 255)
    roll_angle = dict_sensors['orientation']['roll']
    sketch_horizon_line(image, roll_angle, 150, 150)

    
def get_dict_sensors(sense, values):
    values['gyro'] = sense.get_gyroscope()
    values['pressure'] = sense.get_pressure()
    values['temperature'] = sense.get_temperature()
    values['humidity'] = sense.get_humidity()
    values['orientation'] = sense.get_orientation()
    return values
    
telemetry_dict = {'light' : 'OFF'}        
        
if auto:
    yaw_abs = sense.get_accelerometer()['yaw']
    press_abs = sense.get_pressure()
dict_sensors = 0

direction = ''

while True:
    telemetry_dict['direction'] = direction
    frame = vs.read()
    dict_sensors = get_dict_sensors(sense, telemetry_dict)
    display_telemetry(frame, dict_sensors)
    cv2.imshow("ROV", frame)
    
    # The event listener will be running in this block
    key = cv2.waitKey(1) & 0xFF

    if key == ord('q'):
        break
    if key == ord('o'):
        dict_sensors['light'] = 'ON'
    if key == ord('p'):
        dict_sensors['light'] = 'OFF'
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
        direction = ''
        if key == ord('e'):
            direction = 'forward'
            #motor_react(motor_back_dx, green)
            #motor_react(motor_back_sx, green)
        if key == ord('d'):
            direction = 'backward'
            #motor_react(motor_back_dx, red)
            #motor_react(motor_back_sx, red)
        if key == ord('s'):
            direction = 'left'
        if key == ord('f'):
            direction = 'right'
        pass
cv2.destroyAllWindows()
        
    
    

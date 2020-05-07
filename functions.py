import params as p
import cv2
from math import cos, sin, tan, pi, radians

if not p.simulation_mode:
    from sense_hat import SenseHat
else:
    from sense_emu import SenseHat
    
sense = SenseHat()
sense.clear()


def motor_react(motor, color):
    for i in motor:
        sense.set_pixel(i[0], i[1], color)
    return


def lights(status):
    if status:
        motor_react(p.front_lights, p.white)
        return
    motor_react(p.front_lights, p.off)

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
    values['pressure'] = sense.get_pressure()
    values['temperature'] = sense.get_temperature()
    values['humidity'] = sense.get_humidity()
    values['orientation'] = sense.get_orientation()

    # using gyroscope and compass creates a block in the video stream from raspberry when pressed a key 
    #values['gyro'] = sense.get_gyroscope()
    #values['compass_north'] = north = sense.get_compass()
    return values

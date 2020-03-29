# AI-ROV

This project consists in building a first prototype of an AI powered Remotely Operated Vehicle 


## HARDWARE 

The project is curretly running on the following hardware 

- Raspberry PI 4B
- PiCamera
- Raspberry SenseHat (for sensors and to simulate with the leds the motors)



## BASIC FEATURES TO DEVELOP

- Create a gui (on screen display) to display the telemetry 
- Manage motors with Joystick
- Implement motors 
- Implement led managing (activated by keyboard)


## ADVANCED FEATURES TO DEVELOP

- Computer vision based model to detect movements to create a position hold image based
- Reinforcement Learning model to ensure correct position hold (observation_space = sensors, action_space = motors)
- Line edge detection to work in low visibility environment

import random


# SenseHat simulator 
class SenseHat():
    def clear(self):
        return None
    def set_pixel(self, x, y, color):
        return None
    def get_gyroscope(self):
        return {'yaw' : random.randint(0,20), 'roll' : random.randint(0,20), 'pitch' : random.randint(0,20)}
    def get_pressure(self):
        return random.randint(900,1100)
    def get_temperature(self):
        return random.randint(30,50)
    def get_humidity(self):
        return random.randint(30,50)
    def get_orientation(self):
        return {'yaw' : random.randint(0,20), 'roll' : random.randint(0,20), 'pitch' : random.randint(0,20)}
    def get_compass(self):
        return random.randint(0,20)
    def get_accelerometer(self):
        return {'yaw' : random.randint(0,20), 'roll' : random.randint(0,20), 'pitch' : random.randint(0,20)}

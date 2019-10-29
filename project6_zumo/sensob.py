import numpy as np
from project6_supply.PLAB.camera import Camera
from project6_supply.PLAB.ultrasonic import Ultrasonic
from project6_supply.PLAB.reflectance_sensors import ReflectanceSensors


class Sensob:

    def __init__(self, sensor):
        """Initialize sensor"""
        self.sensor = sensor
        self.value = None

    def update(self):
        """Update sensor values"""
        raise NotImplementedError

    def get_value(self):
        """Return sensor value"""
        return self.value

    def reset(self):
        """Set sensor value to None"""
        self.value = None

class UltrasonicSensob(Sensob):

    def __init__(self, sensor):
        """Initialize sensor"""
        super().__init__(sensor)

    def update(self):
        """Update sensor values"""
        if isinstance(Ultrasonic, self.sensor):
            self.value = self.sensor.get_value()



class ReflectanceSensob(Sensob):

    def __init__(self, sensor):
        """Initialize sensor"""
        super().__init__(sensor)

    def update(self):
        """Update sensor values"""
        if isinstance(ReflectanceSensors, self.sensor):
            self.value = self.sensor.get_value()


class CameraSensob(Sensob):

    def __init__(self, sensor):
        """Initialize sensor"""
        super().__init__(sensor)

    def update(self):
        """Update sensor values"""
        colors = {"Red" : 0, "Green" : 0}
        if isinstance(Camera, self.sensor):
            image = self.sensor.get_value()
            hsv_im = image.convert('HSV')
            hsv_na = np.array(hsv_im)
            hsv_value = hsv_na[:, :, 0]
            # Find all red pixels
            red_lo, red_hi = 340, 20
            red_lo = int((red_lo * 255) / 360)
            red_hi = int((red_hi * 255) / 360)
            red = np.where((hsv_value > red_lo) | ((hsv_value < red_hi) & (hsv_value > 1)))
            red_count = red[0].size
            # Find all green pixels
            green_lo, green_hi = 100, 140
            green_lo = int((green_lo * 255) / 360)
            green_hi = int((green_hi * 255) / 360)
            green = np.where((hsv_value > green_lo) & (hsv_value < green_hi))
            green_count = green[0].size
            #Add percentage to color dict
            height, width = image.size
            colors["Red"] = red_count/(height * width)
            colors["Green"] = green_count/(height * width)
            self.value = colors















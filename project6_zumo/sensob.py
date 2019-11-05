"""Contains sensob objects"""
import numpy as np
from PIL import Image


class Sensob:
    """Superclass for sensobs"""
    def __init__(self, sensor):
        """Default init for sensobs"""
        self.sensor = sensor
        self.value = None

    def update(self):
        """Must be implemented in subclasses"""
        raise NotImplementedError

    def get_value(self):
        """Default function for all subclasses"""
        return self.value

    def reset(self):
        """Resets the sensob value"""
        self.value = None


class UltrasonicSensob(Sensob):
    """Ultrasonicsensob object"""
    def __init__(self, sensor):
        """initiates the ultrasonic"""
        super().__init__(sensor)

    def update(self):
        """updates the ultrasonic sensob using the wrapper"""
        self.sensor.update()
        #if isinstance(Ultrasonic, self.sensor):
        dist = self.sensor.get_value()
        if dist > 25:
            dist = 0
        else:
            dist = 1 - dist/25
        self.value = dist
        print("Distance", dist)
        print("Value from ultrasonic sensob:   ", self.value)


class ReflectanceSensob(Sensob):
    """reflectancesensob object"""
    def __init__(self, sensor):
        """Uses super init"""
        super().__init__(sensor)

    def update(self):
        """Updates the values"""
        self.sensor.update()
        sens_array = self.sensor.get_value()
        left_array = sens_array[0:3]
        right_array = sens_array[3:6]
        left_average = sum(left_array)/3
        right_average = sum(right_array)/3
        self.value = [left_average, right_average]
        # print("Values from reflectance sensob:    ", self.value)


class CameraSensob(Sensob):
    """Initiates camerasensob"""
    def __init__(self, sensor):
        """Uses super init"""
        super().__init__(sensor)

    def update(self):
        """Updates the image file and readings"""
        colors = {"Red": 0, "Green": 0}
    #    if isinstance(Camera, self.sensor):
        self.sensor.update()
        image = self.sensor.get_value()
        hs_vim = image.convert('HSV')
        hsv_na = np.array(hs_vim)
        halo = hsv_na[:, :, 0]
        # Find all red pix_sizeels
        red_lo, red_hi = 340, 20
        red_lo = int((red_lo * 255) / 360)
        red_hi = int((red_hi * 255) / 360)
        red = np.where((halo > red_lo) | ((halo < red_hi) & (halo > 1)))
        red_count = red[0].size
        # Find all green pix_sizeels
        green_lo, green_hi = 100, 140
        green_lo = int((green_lo * 255) / 360)
        green_hi = int((green_hi * 255) / 360)
        green = np.where((halo > green_lo) & (halo < green_hi))
        green_count = green[0].size
        # Add percentage to color dict
        x_size, y_size = image.size
        colors["Red"] = red_count/(x_size * y_size)
        colors["Green"] = green_count/(x_size * y_size)
        self.value = colors
        # print("Picture colors: ", colors)

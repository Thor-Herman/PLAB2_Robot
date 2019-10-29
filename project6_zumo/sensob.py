from project6_supply.PLAB.camera import Camera
from project6_supply.PLAB.ultrasonic import Ultrasonic
from project6_supply.PLAB.reflectance_sensors import ReflectanceSensors
from PIL import Image
import numpy as np

class Sensob:

    def __init__(self, sensor):
        self.sensor = sensor
        self.value = None

    def update(self):
        raise NotImplementedError

    def get_value(self):
        return self.value

    def reset(self):
        self.value = None

class UltrasonicSensob(Sensob):

    def __init__(self, sensor):
        super().__init__(sensor)

    def update(self):
        self.sensor.update()
        #if isinstance(Ultrasonic, self.sensor):
        self.value = self.sensor.get_value()



class ReflectanceSensob(Sensob):

    def __init__(self, sensor):
        super().__init__(sensor)

    def update(self):
        self.sensor.update()
        #if isinstance(ReflectanceSensors, self.sensor):
        self.value = self.sensor.get_value()


class CameraSensob(Sensob):

    def __init__(self, sensor):
        super().__init__(sensor)

    def update(self):
        colors = {"Red" : 0, "Green" : 0}
    #    if isinstance(Camera, self.sensor):
        self.sensor.update()
        im = self.sensor.get_value()
        HSVim = im.convert('HSV')
        HSVna = np.array(HSVim)
        H = HSVna[:, :, 0]
        # Find all red pixels
        redLo, redHi = 340, 20
        redLo = int((redLo * 255) / 360)
        redHi = int((redHi * 255) / 360)
        red = np.where((H > redLo) | ((H < redHi) & (H > 1)))
        redCount = red[0].size
        # Find all green pixels
        greenLo, greenHi = 100, 140
        greenLo = int((greenLo * 255) / 360)
        greenHi = int((greenHi * 255) / 360)
        green = np.where((H > greenLo) & (H < greenHi))
        greenCount = green[0].size
        #Add percentage to color dict
        x, y = im.size
        colors["Red"] = redCount/(x * y)
        colors["Green"] = greenCount/(x * y)
        print(colors)
        self.value = colors















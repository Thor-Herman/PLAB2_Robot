from project6_supply.PLAB.camera import Camera
from project6_supply.PLAB.ultrasonic import Ultrasonic
from project6_supply.PLAB.reflectance_sensors import ReflectanceSensors
from PIL import Image

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
        if isinstance(Ultrasonic, self.sensor):
            self.value = self.sensor.get_value()



class ReflectanceSensob(Sensob):

    def __init__(self, sensor):
        super().__init__(sensor)

    def update(self):
        if isinstance(ReflectanceSensors, self.sensor):
            self.value = self.sensor.get_value()


class CameraSensob(Sensob):

    def __init__(self, sensor):
        super().__init__(sensor)

    def update(self):
        colors = {"Red" : 0, "Green" : 0}
        if isinstance(Camera, self.sensor):
            picture = self.sensor.get_value()
            pix = picture.load()
            width, height = picture.size
            for x in range(width):
                for y in range(height):
                    break
                    #To be continued











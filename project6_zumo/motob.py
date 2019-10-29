__author__ = 'SondreOD'
"""Contains the motob object, a controller for motors"""
from project6_supply.PLAB.motors import Motors


class Motob:
    """Interface between arbitrator and motors"""
    def __init__(self):
        self.motor = Motors()
        self.value = []
        self.flag = False

    def update(self, motor_rec):
        """Updates the flag and values, calls operationalize"""
        self.value = motor_rec[0]
        self.flag = motor_rec[1]
        self.operationalize()

    def operationalize(self):
        """Drives the zumo bot forward or backwards depending on values"""
        if self.flag:
            self.motor.stop()
            return
        self.motor.set_value(self.value, 0.5)

"""Contains the motob object, a controller for motors"""
from project6_supply.PLAB.motors import Motors
__author__ = 'SondreOD'


class Motob:
    """Interface between arbitrator and motors"""
    def __init__(self):
        self.motor = Motors()
        self.value = []
        self.flag = False
        # self.recs = {'L': self.motor.left,
        #              'R': self.motor.right,
        #              'F': self.motor.forward,
        #             'B': self.motor.backward,
        #             'S': self.motor.stop}

    def update(self, motor_rec):
        """Updates the flag and values, calls operationalize"""
        print("Motor recommendations:     ", motor_rec)
        self.value = motor_rec[0]
        self.flag = motor_rec[1]
        self.operationalize()

    def operationalize(self):
        """Drives the zumo bot forward or backwards depending on values"""
        if self.flag:
            self.motor.stop()
            return
        self.motor.set_value(self.value, 0.5)

    def stop(self):
        self.motor.stop()

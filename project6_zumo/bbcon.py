"""Contains the bbcon class which will only be instantiated once"""
from time import sleep
from arbitrator import Arbitrator
from motob import Motob


class BBCON:
    """Class for main controller of robot"""
    def __init__(self, sensobs):
        self.behaviors = []
        self.active_behaviors = []
        self.inactive_behaviors = []
        self.sensobs = []
        self.motob = Motob()
        self.arbitrator = Arbitrator()
        self.current_timestep = 0.5

    def add_behavior(self, behavior):
        """Adds a behavior to the list of behaviors"""
        self.behaviors.append(behavior)

    def add_sensob(self, sensob):
        """Adds a sensob to the list of sensobs in use"""
        self.sensobs.append(sensob)

    def activate_behavior(self, behavior):
        """Add behavior to list of active behaviors"""
        self.active_behaviors.append(behavior)

    def deactivate_behavior(self, behavior):
        """Remove behavior from active behaviors"""
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    def update_sensobs(self):
        """Query the sensobs for their values along with preprocessing the values"""
        for sensob in self.sensobs:
            sensob.update()

    def update_behaviors(self):
        """Updates the behaviors in active behaviors"""
        for behavior in self.active_behaviors:
            behavior.update()  # Er dette riktig måte å gjøre det på?

    def update_motobs(self, motor_rec, halt_request):
        """ :param motor_rec contains the motor recommendations
            :param halt_request is a boolean value which decides if robot
            should be shut down
        """
        self.motob.update(motor_rec, halt_request)

    def reset_sensobs(self):
        """Resets the sensobs objects"""
        for sensob in self.sensobs:
            sensob.reset()

    def run_one_timestep(self):
        """Executes a behavior"""
        self.update_sensobs()
        self.update_behaviors()
        motor_rec, halt_req = self.arbitrator.choose_action(self.active_behaviors)
        self.update_motobs(motor_rec, halt_req)
        sleep(self.current_timestep)
        self.reset_sensobs()





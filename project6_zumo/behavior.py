
class Behavior:

    def __init__(self, bbcon, senobs, priority):
        self.bbcon = bbcon
        self.sensobs = senobs
        self.motob_rec = None
        self.active_flag = False
        self.halt_activity = False
        self.priority = priority
        self.match_degree = 0  # Should probably be changed later
        self.weight = self.priority * self.match_degree

    def consider_deactivation(self):
        """Only if activated"""
        pass

    def consider_activation(self):
        """Only if deactivated"""
        pass

    def sense_and_act(self):
        """Main data method"""
        pass

    def update(self):
        """Called each timestep"""
        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()
        if self.active_flag:
            motor_req, match_deg, halt_req = self.sense_and_act()  # Returns three variables in children
            self.motob_rec = motor_req
            self.match_degree = match_deg
            self.halt_activity = halt_req
            self.weight = match_deg * self.priority

    def get_recommendation(self):
        """Returns motor recommendation"""
        return self.motob_rec

    def get_weight(self):
        """Returns weight"""
        return self.weight

    def get_halt(self):
        """Returns halt status"""
        return self.halt_activity


class BackwardsBehavior(Behavior):

    def __init__(self, bbcon, sensobs, priority, sensitivity):
        super().__init__(bbcon, sensobs, priority)  # Sensobs = Camera sensob, Ultrasonic sensob
        self.cam = self.sensobs[0]
        self.sonic = self.sensobs[1]
        self.prev_pic = []  # Record of the previous picture, not sure if needed
        self.longest_distance = 50  # Longest distance the sensor realistically can sense. In cm
        self.motob_rec = [-1, -1]  # Turn backwards
        self.sensitivity = sensitivity  # How large percentage of the image should be green
        self.dist = -10000000000000000000

    def consider_deactivation(self):
        """Only if activated"""
        if self.sonic.get_value()/self.longest_distance > 0.6 or self.cam.get_value()["Green"] < self.sensitivity:  # Arbitrary vals
            self.active_flag = False
            self.bbcon.deactivate_behavior(self)
            #  Should also notify sensob, can only deactivate if both cameras are not needed

    def consider_activation(self):
        """Only if deactivated"""
        if self.sonic.get_value()/self.longest_distance < 0.6 and self.cam.get_value()["Green"] > self.sensitivity:  # Arbitrary vals
            self.active_flag = True
            self.bbcon.activate_behavior(self)
            #  Should also notify sensob

    def sense_and_act(self):
        """Main data method"""
        green_perc = self.cam.get_value()["Green"]
        self.dist = self.sonic.get_value()/self.longest_distance
        motor_req = [-0.25, -0.25]  # Not calculated, can be calculated if necessary
        match_degree = (green_perc + self.dist) * 0.5  # The two % added and then halved
        halt_req = False
        return motor_req, match_degree, halt_req

    def __str__(self):
        return 'BackwardsBehavior, Motor_rec ' + str(self.motob_rec) \
               + "Weight:" + str(self.weight) + "Distance:" + str(self.dist)

class Forward(Behavior):

    def __init__(self, bbcon, sensob, priority):
        super().__init__(bbcon, sensob, priority)  # Sensob is sonic. Only one
        self.longest_distance = 50  # Longest distance the sensor realistically can sense. In cm
        self.active_flag = True

    def consider_activation(self):
        # Possible to make a variable in BBCON which records color, and check that color.
        # If the color is red or green, then this does not need to activate. Otherwise should be active.
        pass

    def consider_deactivation(self):
        pass

    def sense_and_act(self):
        """The closer to an object, the lower the match degree"""
        match_degree = self.sensobs.get_value()/self.longest_distance  # Invers av hvor nærme en er obstruction
        motor_req = [0.25, 0.25]  # Not calculated, can be calculated if necessary
        halt_req = False
        return motor_req, match_degree, halt_req

    def __str__(self):
        return 'ForwardBehavior, Motor_rec ' + str(self.motob_rec) + "Weight:" + str(self.weight)


class Stop(Behavior):

    def __init__(self, bbcon, sensobs, priority, sensitivity):
        super().__init__(bbcon, sensobs, priority)  # Sensobs = Camera sensob, Ultrasonic sensob
        self.cam = self.sensobs[0]
        self.sonic = self.sensobs[1]
        self.prev_pic = []  # Record of the previous picture, not sure if needed
        self.motob_rec = [0, 0]  # Stop the motor
        self.longest_distance = 50  # Longest distance the sensor realistically can sense. In cm
        self.sensitivity = sensitivity  # How large percentage of the image should be green
        self.dist = -1000

    def consider_deactivation(self):
        """Only if activated"""
        if self.sonic.get_value()/self.longest_distance > 0.6 or self.cam.get_value()["Red"] < self.sensitivity:  # Arbitrary vals
            self.active_flag = False
            self.bbcon.deactivate_behavior(self)
            #  Should also notify sensob, can only deactivate if both cameras are not needed

    def consider_activation(self):
        """Only if deactivated"""
        if self.sonic.get_value()/self.longest_distance < 0.6 and self.cam.get_value()["Red"] > self.sensitivity:  # Arbitrary vals
            self.active_flag = True
            self.bbcon.activate_behavior(self)
            #  Should also notify sensob

    def sense_and_act(self):
        """Main data method"""
        green_perc = self.cam.get_value()["Red"]
        self.dist = self.sonic.get_value()/10
        match_degree = (green_perc + (1-self.dist)) * 0.5  # The two % added and then halved
        halt_req = False
        return self.motob_rec, match_degree, halt_req

    def __str__(self):
        return 'StopBehavior, Motor_rec ' + str(self.motob_rec) + "Weight:" + str(self.weight)\
               + "Distance:" + str(self.dist)


class TurnRight(Behavior):

    def __init__(self, bbcon, sensobs, priority):
        super().__init__(bbcon, sensobs, priority)


class TurnLeft(Behavior):

    def __init__(self, bbcon, sensobs, priority):
        super().__init__(bbcon, sensobs, priority)

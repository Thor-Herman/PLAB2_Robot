
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
        self.motob_rec = [-0.5, -0.5]  # Turn backwards
        self.sensitivity = sensitivity  # How large percentage of the image should be green
        self.dist = -1

    def consider_deactivation(self):
        """Only if activated"""
        if self.sonic.get_value() == 0:
            self.active_flag = False
            self.bbcon.deactivate_behavior(self)

    def consider_activation(self):
        """Only if deactivated"""
        if self.sonic.get_value() != 0:
            self.active_flag = True
            self.bbcon.activate_behavior(self)

    def sense_and_act(self):
        """Main data method"""
        green_perc = self.cam.get_value()["Green"]
        self.dist = self.sonic.get_value()
        motor_req = [-0.15, -0.15]  # Not calculated, can be calculated if necessary
        match_degree = (green_perc + self.dist*0.1)  # The two % added and then halved
        if match_degree > 1:
            match_degree = 1
        halt_req = False
        return motor_req, match_degree, halt_req

    def __str__(self):
        return 'BackwardsBehavior, Motor_rec ' + str(self.motob_rec) \
               + "  Weight    :" + str(self.weight) + "   Distance  :" + str(self.dist) +\
               "  Active:   " + str(self.active_flag)


class Forward(Behavior):

    def __init__(self, bbcon, sensob, priority):
        super().__init__(bbcon, sensob, priority)  # Sensob is sonic. Only one
        self.active_flag = True

    def consider_activation(self):
        # if self.sensobs.get_value() == 0:
        #     self.active_flag = True
        #     self.bbcon.activate_behavior(self)
        pass

    def consider_deactivation(self):
        # if self.sensobs.get_value() > 0.6:
        #     self.active_flag = False
        #     self.bbcon.deactivate_behavior(self)
        pass

    def sense_and_act(self):
        """The closer to an object, the lower the match degree"""
        match_degree = 1 - self.sensobs.get_value()  # Invers av hvor nærme en er obstruction
        motor_req = [0.15, 0.15]  # Not calculated, can be calculated if necessary
        halt_req = False
        return motor_req, match_degree, halt_req

    def __str__(self):
        return 'ForwardBehavior, Motor_rec  ' + str(self.motob_rec) + "  Weight:  " + str(self.weight)\
                + "  active:  " + str(self.active_flag)


class Stop(Behavior):

    def __init__(self, bbcon, sensobs, priority, sensitivity):
        super().__init__(bbcon, sensobs, priority)  # Sensobs = Camera sensob, Ultrasonic sensob
        self.cam = self.sensobs[0]
        self.sonic = self.sensobs[1]
        self.prev_pic = []  # Record of the previous picture, not sure if needed
        self.motob_rec = [0, 0]  # Stop the motor
        self.sensitivity = sensitivity  # How large percentage of the image should be green
        self.dist = -1

    def consider_deactivation(self):
        """Only if activated"""
        if self.sonic.get_value() == 0:
            self.active_flag = False
            self.bbcon.deactivate_behavior(self)
            self.bbcon.sensobs.remove(self.cam)

    def consider_activation(self):
        """Only if deactivated"""
        if self.sonic.get_value() > 0.001:
            self.active_flag = True
            self.bbcon.activate_behavior(self)
            self.bbcon.sensobs.append(self.cam)

    def sense_and_act(self):
        """Main data method"""
        green_perc = self.cam.get_value()["Red"]
        self.dist = self.sonic.get_value()
        match_degree = (green_perc + self.dist*0.1) # The two % added and then halved
        if match_degree > 1:
            match_degree = 1
        halt_req = False
        return self.motob_rec, match_degree, halt_req

    def __str__(self):
        return 'StopBehavior, Motor_rec ' + str(self.motob_rec) + "  Weight:  " + str(self.weight)\
               + "  Distance:  " + str(self.dist) + "  Active:  " + str(self.active_flag)


class Turn(Behavior):

    def __init__(self, bbcon, sensobs, priority):
        super().__init__(bbcon, sensobs, priority)
        self.margin = 0.07
        self.sensob_values = []
        self.constant_a = 3
        self.active_flag = True
        self.bbcon.activate_behavior(self)

    def consider_activation(self):
        # if self.difference > self.margin:
        #     self.active_flag = True
        #     self.bbcon.activate_behavior(self)
        pass

    def consider_deactivation(self):
        # if self.difference < self.margin:
        #     self.active_flag = False
        #     self.bbcon.deactivate_behavior(self)'
        pass

    def sense_and_act(self):
        direction = self.compute()
        if direction == -1:
            motob_rec = [-0.20, 0.35]
        elif direction == 1:
            motob_rec = [0.35, -0.20]
        else:
            motob_rec = [0.15, 0.15]
        match_degree = abs(self.difference)*4 + sum(self.sensob_values)/5
        if match_degree > 1:
            match_degree = 1
        halt_req = False
        return motob_rec, match_degree, halt_req

    def compute(self):
        if abs(self.difference) < self.margin:
            return 0
        elif self.difference < 0:
            return -1
        return 1

    def update(self):
        """Called each timestep"""
        self.sensob_values = self.sensobs.get_value()
        self.difference = self.sensob_values[0] - self.sensob_values[1]
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

    def __str__(self):
        return 'TurnBehavior, Motor_rec ' + str(self.motob_rec) + "Weight:" + str(self.weight) \
               + "Values:" + str(self.sensob_values) + "Active: " + str(self.active_flag)

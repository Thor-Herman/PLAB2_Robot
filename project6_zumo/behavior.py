
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
            motor_req, match_deg, halt_req = self.sense_and_act()
            self.motob_rec = motor_req
            self.match_degree = match_deg
            self.halt_activity = halt_req

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
        self.motob_rec = (-1, -1)  # Turn backwards
        self.sensitivity = sensitivity  # How large percentage of the image should be green

    def consider_deactivation(self):
        """Only if activated"""
        if self.sonic.get_value() < 0.6 or self.process_image(self.cam.get_value()) < 0.3:  # Arbitrary vals
            self.active_flag = False
            self.bbcon.deactive_behavior(self)
            #  Should also notify sensob, can only deactivate if both cameras are not needed

    def consider_activation(self):
        """Only if deactivated"""
        if self.sonic.get_value > 0.6 and self.process_image(self.cam.get_value) > 0.3:  # Arbitrary vals
            self.active_flag = True
            self.bbcon.activate_behavior(self)
            #  Should also notify sensob

    def sense_and_act(self):
        """Main data method"""

    def process_image(self, camera_readings):
        """Returns the percentage of the image that is green"""
        
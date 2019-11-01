__author__ = "Thor-Herman"

from project6_zumo.bbcon import BBCON
from project6_zumo.sensob import CameraSensob, UltrasonicSensob, ReflectanceSensob
from project6_supply.PLAB.camera import Camera
from project6_supply.PLAB.ultrasonic import Ultrasonic
from project6_supply.PLAB.reflectance_sensors import ReflectanceSensors
from project6_zumo.behavior import *
from project6_supply.PLAB.zumo_button import ZumoButton


def main():
    ZumoButton().wait_for_press()
    sensobs = create_sensors()
    bbcon = BBCON(sensobs)
    behav_list = create_behaviors(bbcon, sensobs)
    for behav in behav_list:
        bbcon.add_behavior(behav)
        bbcon.activate_behavior(behav)
    while True:
        bbcon.run_one_timestep()


def create_sensors():
    cam_sens = Camera()
    us_sens = Ultrasonic()
    refl_sens = ReflectanceSensors()
    ultrasonic_sensob = UltrasonicSensob(us_sens)
    camera_sensob = CameraSensob(cam_sens)
    reflectance_sensob = ReflectanceSensob(refl_sens)
    sensobs = [camera_sensob, ultrasonic_sensob, reflectance_sensob]
    return sensobs


def create_behaviors(bbcon, sensobs):
    forward_behav = Forward(bbcon, sensobs[1], 1)
    backward_behav = BackwardsBehavior(bbcon, sensobs[0:2], 1, 0.3)
    stop_behav = Stop(bbcon, sensobs[0:2], 1, 0.3)
    turn_behav = Turn(bbcon, sensobs[2], 1)
    return [forward_behav, backward_behav, stop_behav, turn_behav]


if __name__ == '__main__':
    main()


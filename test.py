import time
from project6_zumo.motob import Motob
from project6_supply.PLAB.zumo_button import ZumoButton


def main():
    ZumoButton().wait_for_press()
    motob = Motob()
    while 1:
        time.sleep(0.5)
        motob.update(([0.25, 0.25], False))


if __name__ == '__main__':
    main()

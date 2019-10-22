class Arbitrator:
    """Arbitrator finds the best behavior and returns it"""
    @staticmethod
    def choose_action(behaviour_list):
        """Chooses which behaviour wins"""
        heaviest_behaviour = ''
        for behaviour in behaviour_list:
            if behaviour.get_weight() > heaviest_behaviour.get_weight():
                heaviest_behaviour = behaviour
        best_choice = (heaviest_behaviour.get_motor_recommendations(), heaviest_behaviour.get_halt())
        return best_choice

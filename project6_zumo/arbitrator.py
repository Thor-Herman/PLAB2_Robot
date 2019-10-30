class Arbitrator:
    """Arbitrator finds the best behavior and returns it"""
    @staticmethod
    def choose_action(behaviour_list):
        """Chooses which behaviour wins"""
        heaviest_behaviour = behaviour_list[0]
        for behaviour in behaviour_list:
            print(behaviour)
            if behaviour.get_weight() > heaviest_behaviour.get_weight():
                heaviest_behaviour = behaviour
        best_choice = (heaviest_behaviour.get_recommendation(), heaviest_behaviour.get_halt())
        return best_choice

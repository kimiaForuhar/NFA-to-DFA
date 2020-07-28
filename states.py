class State:
    def __init__(self, name):
        # dictionary with keys of transiotion chars, and values consisting the states reachable from mentioned char
        self.deltas = {}

        # name of the following state
        self.name = name

        # real_states are the participant states of a bigger state, for instance "q0q1" has the real states "q0" and "q1"
        self.real_states = set()
        self.isFinal = False

    def add_delta(self, state, char):
        if char not in self.deltas:
            self.deltas[char] = set()
        self.deltas[char].add(state)

    def add_real_state(self, name):
        self.real_states.add(name)

    def set_final(self):
        self.isFinal = True

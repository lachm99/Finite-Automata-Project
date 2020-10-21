class State(object):
    """
    State Class
    -----------
    Represents Finite Automata State, (Graph Vertex).

    Attributes:
        * name   (String): The id/name of this state
        * deltas (list)  : List of deltas (edges) incident on this state.
        * isFinal(bool)  : Whether this State is in the list of final states.
    """
    def __init__(self, name):
        self.name = name
        self.deltas = []
        self.closure = set([])
        self.is_final = False

    def __eq__(self, compare):
        if (isinstance(compare, State)):
            return self.name == compare.name
        else:
            # Compared to STRING name
            return self.name ==compare

    def __repr__(self):
        return self.name

    def __hash__(self):
        return hash(repr(self))

    def add_delta(self, d):
        self.deltas.append(d)

    def remove_delta(self, d):
        self.deltas.remove(d)

    def set_final(self, is_final):
        self.is_final = is_final

class SuperState(State):
    """
    SuperState Class
    ----------------
    Actually extends state - but is a state that represents a set of states
    """
    def __init__(self, name, states):
        super().__init__(name)
        self.substates = states
        self.is_final = True in [state.is_final for state in states]

    def __hash__(self):
        return hash(self.name)

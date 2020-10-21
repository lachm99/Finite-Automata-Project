class State:
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
        self.isFinal = False

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

    def setFinal(self, isFinal):
        self.isFinal = isFinal

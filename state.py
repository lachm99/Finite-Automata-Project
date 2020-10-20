class State:
    """
    State Class
    -----------
    Represents Finite Automata State, (Graph Vertex).

    Attributes:
        * name   (String): The id/name of this state
        * deltas (list)  : List of deltas (edges) incident on this state.
    """
    def __init__(self, name):
        self.name = name
        self.deltas = []

    def __eq__(self, compare):
        if (isinstance(compare, State)):
            return self.name == compare.name
        else:
            # Compared to STRING name
            return self.name ==compare

    def __repr__(self):
        return self.name

    def add_delta(self, d):
        self.deltas.append(d)

    def remove_delta(self, d):
        self.deltas.remove(d)


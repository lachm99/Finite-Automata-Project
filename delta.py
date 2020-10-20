class Delta:
    """
    Delta Class
    -----------
    Represents transition delta (Graph Edge).

    Attributes:
        * start  (State) : The State (vertex) this delta exits from
        * symbol (String): The Alpha symbol via which this transition occurs
        * end    (State) : The State (vertex) this delter enters into
    """
    def __init__(self, start, symbol, end):
        self.start = start
        self.symbol = symbol
        self.end = end

    def __eq__(self, compare):
        return (self.symbol == compare.symbol and
                self.start == compare.start and
                self.end == compare.end)

    def __repr__(self):
        return "{},{},{}".format(self.start.name, self.symbol, self.end.name)

    def transition_unique(deltas, transition):
        for delta in deltas:
            if (transition == delta):
                return False
        return True




class DFA:
    def __init__(self, states, alpha, start, final, deltas):
        self.states = set(states)
        self.alpha = set(alpha)
        self.start = start
        self.final = set(final)
        self.deltas = deltas

    def __repr__(self):
        out = ",".join(sorted(self.states)) + "\n"
        out += ",".join(sorted(self.alpha)) + "\n"
        out += self.start + "\n"
        out += ",".join(sorted(self.final)) + "\n"
        for state in sorted(self.deltas):
            for alpha in sorted(self.deltas[state]):
                for reached in self.deltas[state][alpha]:
                    out += "{},{},{}\n".format(state, alpha, reached)
        out += "end"
        return out

    def traverse_string(self, state, instring):
        for a in instring:
            stateset = self.deltas[state][a]
            state = list(stateset)[0]
        return state

    def accepts(self, string):
        if (self.traverse_string(self.start, string) in self.final):
            return 1
        return 0

class NFA:
    def __init__(self, states, alpha, start, final, deltas):
        self.states = set(states)
        self.alpha = set(alpha)
        self.start = start
        self.final = set(final)
        self.deltas = deltas
        self.closures = dict.fromkeys(states, set([]))

    def traverse(self, origin, symbol):
        reached = set([])
        if (symbol in self.deltas[origin]):
            reached = self.deltas[origin][symbol]
        return reached

    def traverse_string(self, origin, string):
        states = set([origin])
        for a in string:
            reached = set([])
            for state in states:
                reached = reached | self.traverse(state, a)
            states = reached
        return reached

    def compute_closure(self):
        for state in self.states:
            self.recurse_closure(state, [], state)

    def recurse_closure(self, origin, visited, state):
        if state in visited:
            return
        visited.append(state)
        if (len(self.closures[state] > 0)):
            self.closures[origin] |= self.closures[state]
            return
        self.closures[origin].add(state)
        if "" in self.deltas[state]:
            for target in list(self.deltas[state][""]):
                self.recurse_closure(origin, visited, target)





























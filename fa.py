
import string
class FA(object):
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


    def nfa_to_dfa(nfa):
        start = frozenset([nfa.start])
        Q = set([start])
        unprocessedQ = Q.copy()
        states = set([])
        new_states = {}
        deltas = {}
        final = []
        alpha = nfa.alpha

        while len(unprocessedQ) > 0:
            qSet = unprocessedQ.pop()
            deltas[qSet] = {}
            for a in list(alpha):
                reached = set([])
                for q in qSet:
                    end_states = nfa.traverse(q,a)
                    reached.update(end_states)
                reached = frozenset(reached)
                deltas[qSet][a] = reached
                if not reached in Q:
                    Q.add(reached)
                    unprocessedQ.add(reached)
        for qSet in Q:
            if len(qSet & nfa.final) > 0:
                final.append(qSet)

        i=0
        new_deltas = dict.fromkeys([key for key in sorted(deltas)])
        for d in new_deltas:
            new_deltas[d] = (i//26 + 1) * string.ascii_uppercase[i%26]
            i+=1

        start_named = new_deltas[start]
        final_named = [new_deltas[f] for f in final]
        deltas_named = {}
        for s in deltas:
            deltas_named[new_deltas[s]] = dict.fromkeys([a for a in sorted(alpha)])
            for a in deltas[s]:
                target_state = deltas_named[new_deltas[s]]
                target_state[a]
                deltas_named[new_deltas[s]][a] = new_deltas[deltas[s][a]]

        dfa = DFA([key for key in deltas_named], alpha, start_named, final_named, deltas_named)
        return dfa

class DFA(FA):
    def __init__(self, states, alpha, start, final, deltas):
        super().__init__(states, alpha, start, final, deltas)

    def traverse_string(self, state, instring):
        for a in instring:
            stateset = self.deltas[state][a]
            state = list(stateset)[0]
        return state

    def accepts(self, string):
        if (self.traverse_string(self.start, string) in self.final):
            return 1
        return 0

class NFA(FA):
    def __init__(self, states, alpha, start, final, deltas):
        super().__init__(states, alpha, start, final, deltas)
        self.closures = dict.fromkeys(states)
        for s in states:
            self.closures[s] = set([])

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

    def generate_efnfa(self):


        return efnfa

    def compute_closures(self):
        for state in self.states:
            self.recurse_closure(state, [], state)

    def recurse_closure(self, origin, visited, state):
        if state in visited:
            return
        visited.append(state)
        if (len(self.closures[state]) > 0):
            self.closures[origin] |= self.closures[state]
            return
        self.closures[origin].add(state)
        if "" in self.deltas[state]:
            for target in list(self.deltas[state][""]):
                self.recurse_closure(origin, visited, target)


    def print_closures(self):
        for state in sorted(self.closures):
            print(state + ":" + ",".join(sorted(self.closures[state])))
        print("end")

























""" A module containing finite automata related classes """

from state import State, SuperState
from delta import Delta
import string

class FA(object):
    """
    Finite Automata Class
    ---------------------
    Attributes:
        * states (list) : A list of States (Vertices) in the FA
        * alpha  (list) : A list of symbols in the FA's alphabet
        * start  (State): The single start state for this FA
        * final  (list) : The set of accept states for this FA

    """
    def __init__(self, iterator = None):
        self.states = []
        self.alpha = []
        self.start = None
        self.final = set([])
        # If init'd without iterator, return skeleton FA
        if (iterator == None):
            return
        # Else, populate FA by generating from the provided input iterator
        self.generate(iterator)

    def __repr__(self):
        out = ",".join([repr(state) for state in self.states]) + "\n"
        out += ",".join(self.alpha) + "\n"
        out += repr(self.start) + "\n"
        out += ",".join([repr(state) for state in self.final]) + "\n"
        for state in self.states:
            if (state.deltas == []):
                continue
            out += "\n".join([repr(delta) for delta in state.deltas]) + "\n"
        out += "end"
        return out

    def generate(self, itr):
        self.states = [State(name) for name in next(itr).split(',')]
        self.alpha = next(itr).split(',')
        self.start = self.find_state(next(itr))
        [self.insert_final(self.find_state(name)) for name in next(itr).split(',')]
        self.generate_deltas(itr)

    def generate_deltas(self, itr):
        # Create transitions from comma separated lines of information.
        for line in itr:
            # Interpret start state, transition symbol, termination state.
            s_name, symbol, e_name = line.split(',')
            start = self.find_state(s_name)
            end = self.find_state(e_name)
            FA.insert_delta(start, symbol, end)

    def insert_delta(start, symbol, end):
        new_delta = Delta(start, symbol, end)
        for d in start.deltas:
            if (new_delta == d):
                # If it already exists, don't add a new one!
                return
        start.deltas.append(new_delta)

    def insert_final(self, state):
        self.final.add(state)
        state.set_final(True)

    def find_state(self, state_name):
        for state in self.states:
            if (state == state_name):
                return state


    """
    ===============================
    OLD METHODS. Might Reimplement.
    ===============================
    def deep_copy(self):
        copy = FAset()
        copy.states = dict()
        for state in self.states:
            copy.states[state] = (self.states[state][0].copy(),
                                  self.states[state][1].copy())
        copy.final_states = self.final_states.copy()
        copy.start_state = self.start_state
        copy.alpha = self.alpha.copy()
        return copy

    def copy_without_deltas(self):
        copy = FA()
        copy.states = dict()
        for state in self.states:
            copy.states[state] = (set(),
                                  self.states[state][1].copy())
        copy.final_states = self.final_states.copy()
        copy.start_state = self.start_state
        copy.alpha = self.alpha.copy()
        return copy
    ===============================
    OLD METHODS. Might Reimplement.
    ===============================
    """



class NFA(FA):
    """
    NFA Class: Subclass of FA.
    --------------------------
    """
    def __init__(self, iterator = None):
        super().__init__(iterator)

    def assign_closures(self, closures):
        for key in closures:
            state = self.find_state(key)
            for reached in closures[key]:
                state.closure.add(self.find_state(reached))

    def compute_closures(self):
        for state in self.states:
            self.recurse_e_closure(state, [], state)
        return

    def recurse_e_closure(self, origin, visited, state):
        if (state in visited):
            return
        visited.append(state)
        # If we encounter a state with already calculated e_clos,
        # don't recalculate! just union its result
        if (len(state.closure) > 0):
            origin.closure.update(state.closure)
            return
        origin.closure.add(state)
        for delta in state.deltas:
            if (delta.symbol == ""):
                self.recurse_e_closure(origin, visited, delta.end)

    def transform_to_efnfa(self):
        for origin in self.states:
            for state in list(origin.closure):
                if (state.is_final):
                    self.insert_final(origin)
                """
                if (state == origin):
                    continue
                """
                for delta in state.deltas.copy():
                    if (delta.symbol == ""):
                        state.remove_delta(delta)
                    else:
                        FA.insert_delta(origin, delta.symbol, delta.end)


    """
    def gen_efnfa(self):
        # Start by duplicating the existing nfa
        efnfa = self.copy_without_deltas()
        for state in self.states:
        # Modify original NFA to add direct epsilon transitions from
        # each state to all states in its epsilon closure.
            deltas = self.states[state][0]
            closure = self.states[state][1]
            for reached in closure:
                if (reached == state):
                    continue
                t = Transition("", reached)
                if (Transition.transition_unique(deltas, t)):
                    deltas.add(t)
        for v1 in  self.states:
            deltas1 = self.states[v1][0]
            for delta1 in deltas1:
                if (delta1.string == ""):
                    v2 = delta1.end
                    deltas2 = self.states[v2][0]
                    for delta2 in deltas2:
                        if (delta2.string != ""):
                            # Create new transition,
                            # Add it to EFNFA!
                            t = Transition(delta2.string, delta2.end)
                            # if (Transition.transition_unique(deltas1, t)):
                            efnfa.states[v1][0].add(t)
                    if (v2 in self.final_states):
                        efnfa.final_states.add(v1)
                else:
                    efnfa.states[v1][0].add(t)
        return efnfa
    """

    def print_closures(self):
        output = ""
        for state in self.states:
            output += repr(state) + ":"
            for val in state.closure:
                output += repr(val) + ","
            output = output.rstrip(",") + "\n"
        output += "end"
        print(output)



class DFA(FA):
    """
    DFA Class: Subclass of FA.
    --------------------------
    """
    def __init__(self, iterator = None):
        super().__init__(iterator)

    def NFA_to_DFA(nfa):
        dfa = DFA()
        sigma = list(string.ascii_uppercase)
        i = 0
        dfa.alpha = nfa.alpha

        start_state = frozenset([nfa.start])

        q0 = SuperState(sigma[i], start_state)
        dfa.states.append(q0)
        dfa.start = q0
        i+=1

        unprocessed = set([q0])
        processed = set()

        while (len(unprocessed) > 0):
            qSuper = unprocessed.pop()
            processed.add(qSuper)
            for a in nfa.alpha:
                reached = []
                # Find all states reached by letter a from all the states in qSet
                for q in qSuper.substates:
                    for delta in q.deltas:
                        if (delta.symbol == a):
                            reached.append(delta.end)

                if set(reached) not in [set(sup.substates) for sup in processed]:
                    qSuper2 = SuperState(sigma[i], reached)
                    i += 1
                    unprocessed.add(qSuper2)
                    dfa.insert_state(qSuper2)
                    FA.insert_delta(qSuper, a, qSuper2)

        return dfa

    def insert_state(self, state):
        self.states.append(state)
        if (state.is_final):
            self.final.add(state)



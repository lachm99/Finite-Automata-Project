""" A module containing finite automata related classes """

class FA(object):
    """ Finite Automata contains:
        States, A dictionary with:
            Key: state names
            Value: Tuple containing - State delta set, state epsilon closure
        Alphabet,
        Start state,
        Set of final states.

        Can be Initialised with or without an iterator - to construct from
        user input, or to be manually constructed (eg. when copied)
    """
    def __init__(self, iterator = None):
        self.states = dict()
        self.alpha = set()
        self.start_state = None
        self.final_states = set()
        # If init'd without iterator, must be wanting a blank copy.
        if (iterator == None):
            return

        self.gen_states(next(iterator).split(','))
        self.assign_alpha(next(iterator).split(','))
        self.assign_start(next(iterator))
        self.assign_final(next(iterator).split(','))
        self.gen_deltas(iterator)

    def gen_states(self, names):
        # Initialise states based on the provided names
        self.states = dict.fromkeys(names)
        for key in self.states:
            # Each entry has a tuple of sets containing 
            # transitions from this state, and e-closure of the state.
            self.states[key] = (set(), set())

    def assign_alpha(self, alphas):
        self.alpha = set(alphas)

    def assign_start(self, start_name):
        self.start_state = start_name

    def assign_final(self, final_name_array):
        self.final_states.update(set(final_name_array))

    def gen_deltas(self, lines):
        # Create transitions from comma separated lines of information.
        for line in lines:
            # Interpret start state, transition symbol, termination state.
            s, c, t = line.split(',')
            # Add to state s's transitions, the transition over c to t.
            self.states[s][0].add(Transition(c,t))

    def deep_copy(self):
        copy = FA()
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

    def print_fa(self):
        output = [""]*5
        for state in self.states:
            output[0] += state + ","
        output[0] = output[0].rstrip(",")
        for a in self.alpha:
            output[1] += a + ","
        output[1] = output[1].rstrip(",")
        output[2] += self.start_state
        for state in sorted(self.final_states):
            output[3] += state + ","
        output[3] = output[3].rstrip(",")

        for state in sorted(self.states):
            deltas = self.states[state][0]
            for delta in deltas:
                output[4] += f"{state},{delta.string},{delta.end}\n"
        output[4] += "end"

        [print(line) for line in output]

class NFA(FA):
    """ Subclass of FA.
        Contains methods for calculating or assigning epsilon closures,
        Generating an epsilon free NFA from itself,
    """
    def __init__(self, it):
        super().__init__(it)

    def assign_closures(self, closures):
        for state in closures:
            self.states[state][1].update(closures[state])

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
        if (len(self.states[state][1]) > 0):
            self.states[origin][1].update(self.states[state][1])
            return
        self.states[origin][1].add(state)
        for delta in self.states[state][0]:
            if (delta.string == ""):
                self.recurse_e_closure(origin, visited, delta.end)

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

    def print_closures(self):
        output = ""
        for state in self.states:
            output += state + ":"
            for val in sorted(self.states[state][1]):
                output += val + ","
            output = output.rstrip(",") + "\n"
        output += "end"
        print(output)



class DFA(FA):
    def __init__(self, it):
        super().__init__(it)

    def NFA_to_DFA(nfa):
        # Given an EFNFA, construct a corresp. DFA
        

        return dfa


class Transition:
    """ Automata Transition (delta) Object. Contains:
        End state name
        A transition string.
    """
    def __init__(self, string, end):
        self.end = end
        self.string = string

    def equals(self, compare):
        if (self.string == compare.string and self.end == compare.end):
            return True
        return False

    def transition_unique(deltas, transition):
        for delta in deltas:
            if (transition.equals(delta)):
                return False
        return True


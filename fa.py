"""
Finite Automata Module
======================
A module containing FA class, and subclasses NFA and DFA.
Contains methods for computing E-closures, generating EFNA,
Converting EFNFA into equivalent DFA, traversing a DFA on a given string.
"""
import string

class FA(object):
    """
    Finite Automata Class
    ---------------------
    Attributes:
        * states (set) : A set of States (Vertices) in the FA
        * alpha  (set) : A set of symbols in the FA's alphabet
        * start  (Str) : The single start state name for this FA
        * final  (set) : The set of accept state names for this FA
		* deltas (dict): A dictionary containing the transitions for this state.
                         Key: start state name,
                         Val: dictionary containing:
                            Key: transition symbol,
                            Val: Set of reachable states.
    """
    def __init__(self, states, alpha, start, final, deltas):
        self.states = set(states)
        self.alpha = set(alpha)
        self.start = start
        self.final = set(final)
        self.deltas = deltas

    def __repr__(self):
        """
        The method called when the FA is printed, or repr() is called upon it.
        Returns a prettily formatted string representing the components of the FA.
        """
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
        """
        A method for converting the supplied NFA into a corresponding DFA.
        """
        states = set([])
        alpha = nfa.alpha
        start = nfa.start
        final = set([])
        deltas = {}

        # Init some processing queues
        processed = set([])
        unprocessed = set([])
        unprocessed.add(frozenset([start]))

        while len(unprocessed) > 0:
            stateSet = unprocessed.pop()
            processed.add(qSet)
            # Init a dict of deltas originating from this stateset
            deltas[stateSet] = {}
            # For each symbol in the alphabet, find which set of states can be reached.
            for a in list(alpha):
                reached = set([])
                # Add reachable states through a from all states in new stateset
                [reached.update(nfa.traverse(q,a) for q in stateSet)]
                reached = frozenset(reached)
                # Deltas from this stateset across a reaches the set of those states.
                deltas[stateSet][a] = reached
                if not (reached in processed):
                    unprocessed.add(reached)

        for stateSet in processed:
            # Check if the intersection is non-empty (One of the NFA states in this
            # new DFA state was considered final) - add this new state to final.
            if (len(stateSet & nfa.final) > 0):
                final.add(stateSet)
        """
        The states are currently unnamed - just sets of original states.
        Reassign names to states and therefore deltas etc.
        """
        i=0
        new_names = dict.fromkeys([stateSet for stateSet in sorted(deltas)])
        for stateSet in new_names:
            new_names[stateSet] = (1 + i//26) * string.ascii_uppercase[i%26]
            i+=1

        states_named = [new_names[stateSet] for stateSet in new_names]
        start_named = new_names[start]
        final_named.addall([new_names[state] for state in final])
        deltas_named = {}
        for s in deltas:
            deltas_named[new_names[s]] = dict.fromkeys([a for a in sorted(alpha)])
            for a in deltas[s]:
                target_state = deltas_named[new_names[s]]
                target_state[a]
                deltas_named[new_names[s]][a] = new_names[deltas[s][a]]

        return DFA(states_named, alpha, start_named, final_named, deltas_named)


class DFA(FA):
    """
    Deterministic Finite Automata Class
    -----------------------------------
    SUBCLASS of FA. Inherits all attributes.
    """
    def __init__(self, states, alpha, start, final, deltas):
        super().__init__(states, alpha, start, final, deltas)

    def traverse_string(self, state, instring):
        """
        Given a string comprised of the alphabet of the DFA, feeds the DFA
        until the string is consumed, and returns the state which it ends at.
        Since it is a DFA, every delta's stateset over a must have
        EXACTLY ONE STATE.
        """
        for a in instring:
            stateSet = self.deltas[state][a]
            state = list(stateSet)[0]
        return state

    def accepts(self, string):
        """
        Traverses the given string and checks if the returned state
        is in the set of final states for this dfa.
        Returns the relevant output to be printed.
        """
        if (self.traverse_string(self.start, string) in self.final):
            return 1
        return 0



class NFA(FA):
    """
    Non-Deterministic Finite Automata Class
    -----------------------------------
    SUBCLASS of FA. Inherits all attributes.
    Additional Attributes:
        * closures (dict): A dictionary where
                           Key: State name
                           Value: list of state names in the e-closure of key.
    """
    def __init__(self, states, alpha, start, final, deltas):
        super().__init__(states, alpha, start, final, deltas)
        self.closures = dict.fromkeys(states)
        for s in states:
            self.closures[s] = set([])

    def traverse(self, origin, symbol):
        """
        Given the specified input symbol, return the set of states
        reachable from the origin state.
        """
        reached = set([])
        if (symbol in self.deltas[origin]):
            reached = self.deltas[origin][symbol]
        return reached

    def traverse_string(self, origin, string):
        """
        Given the specified input string, return the set of all states
        reachable from the given origin state.
        """
        states = set([origin])
        for a in string:
            reached = set([])
            for state in states:
                reached = reached | self.traverse(state, a)
            states = reached
        return reached

    def transform_to_efnfa(self):
        """
        Mutate this NFA to contain no epsilon closures.
        We make heavy use of the supplied epsilon closures dict.
        """
        for origin in self.closures:
            for state in self.closures[origin]:
                if state in self.final:
                    self.final.update(set([origin]))
                # Iterate through the outgoing transition symbols from the
                # state (in the origins epsilon closure)
                for symbol in self.deltas[state].copy():
                    if (symbol == ""):
                        # If it's an epsilon transition, remove it from the NFA.
                        self.deltas[state].pop("")
                    else:
                        # New delta from origin to this deltas dest across the symbol.
                        if (symbol in self.deltas[origin]):
                            self.deltas[origin][symbol].update(self.deltas[state][symbol])
                        else:
                            self.deltas[origin][symbol] = set(self.deltas[state][symbol])

    def assign_closures(self, closures):
        self.closures = closures

    def compute_closures(self):
        """
        Recursively calculates the e-closures for each state in the NFA
        """
        for state in self.states:
            self.recurse_closure(state, [], state)

    def recurse_closure(self, origin, visited, state):
        """"
        Effectively a recursive graph traversal method
        """
        if state in visited:
            return
        visited.append(state)
        if (len(self.closures[state]) > 0):
            # If the closure for this state has already been calculated, don't
            # recalculate - just include all those states in origins closure.
            self.closures[origin] |= self.closures[state]
            return
        self.closures[origin].add(state)
        if ("" in self.deltas[state]):
            # If there are any e-transitions from the state, recurse on them.
            for target in list(self.deltas[state][""]):
                self.recurse_closure(origin, visited, target)


    def print_closures(self):
        """
        Outputs closures in the form 'Q1:Q1,Qx,Qy,Qz'
        """
        for state in sorted(self.closures):
            print(state + ":" + ",".join(sorted(self.closures[state])))
        print("end")


""" A module containing finite automata related classes """



class FA:
    """ Finite Automata:
        States,
        Alphabet,
        Start state,
        Set of final states.

        Deltas are stored by the state they transition FROM."""
    def __init__(self):
        self.states = []
        self.alpha = []
        self.start_state = None
        self.final_states = []

    def gen_FA(self, iterator):
        # Given an iterator, (over input lines), generate the automata
        self.gen_states(next(iterator).split(','))
        self.gen_alpha(next(iterator).split(','))
        self.assign_start(next(iterator))
        self.assign_final(next(iterator).split(','))
        self.gen_deltas(iterator)

    def gen_states(self, names):
        # Initialise empty states based on the provided names
        for name in names:
            self.states.append(State(name))

    def gen_alpha(self, alphas):
        # Store input array of alphabets into instance var array
        for alpha in alphas:
            self.alpha.append(alpha)

    def assign_start(self, start_name):
        # Find the State object corresponding to the string name
        for state in self.states:
            if (state.name == start_name):
                # Assign automata start state to the object.
                self.start_state = state

    def assign_final(self, final_name_array):
        # Given a list of final state names, make corresponding obj's final.
        for state in self.states:
            if state.name in final_name_array:
                self.final_states.append(state)
                state.set_final()

    def gen_deltas(self, lines):
        # Create transitions from comma separated lines of information.
        for line in lines:
            # init target State objects to null
            s_obj = None;
            t_obj = None;
            # Parse start state name, transition str, terminate state name
            s, c, t = line.split(',')

            # Find corresponding state objs and assign them
            for state in self.states:
                if (state.name == s):
                    s_obj = state
                if (state.name == t):
                    t_obj = state
                # Break if both are found
                if (s_obj != None and t_obj != None):
                    break;

            # Assign a new transition to the starting state.
            s_obj.new_transition(t_obj, c)
            continue;

    def compute_closures(self):
        for state in self.states:
            FA.recurse_e_closure(state, [], state)
        return

    def recurse_e_closure(origin, visited, state):
        if (state in visited):
            return
        # If we encounter a state with already calculated e_clos,
        # don't recalculate! just use it's calcs.
        if (len(state.e_closure) > 0):
            origin.e_closure.update(state.e_closure)
            return
        origin.e_closure.add(state)
        visited.append(state)
        for delta in state.transitions:
            if (delta.string == ""):
                FA.recurse_e_closure(origin, visited, delta.end)

class State:
    """ Automata State Object. Contains:
        String name,
        List of Transitions FROM this state (deltas)
        Boolean value storing if this is a final state. """
    def __init__(self, name):
        self.name = name
        self.transitions = []
        self.final = False
        self.e_closure = set({})

    def set_final(self):
        # Simply set this state to be final
        self.final = True

    def new_transition(self, end, string):
        # Create a new outgoing transition from this state.
        self.transitions.append(Transition(end, string))



class Transition:
    """ Automata Transition (delta) Object. Contains:
        A State object the transition ends at,
        A transition string.

        The start state of the transition is not stored since the 
        start state is what stores this Transition object in every case. """
    def __init__(self, end, string):
        self.end = end
        self.string = string



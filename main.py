"""This module is the entry point to your assignment. There is some scaffolding
to help you get started. It will call the appropriate method (task_1, 2 etc.)
and load the input data. You can edit or remove as much of this code as you
wish to."""

from parser import Parser
from sys import stdin

# Local module containing Finite Automata classes
from fa import *

def task_1(parser):
    """For each state of the NFA, compute the Epsilon closure and output
    it as a line of the form s:a,b,c where s is the state, and {a,b,c} is E(s)"""
    nfa = parser.parse_fa()
    nfa.compute_closures()
    output = ""
    for state in nfa.states:
        output += state.name + ":"
        for x in state.e_closure:
            output += x.name + ","
        output = output.rstrip(",") + "\n"
    output += "end"
    print(output)

def task_2(parser):
    """Construct and output an equivalent Epsilon free NFA.
    The state names should not change."""
    nfa = parser.parse_fa()
    closures = parser.parse_closures()
    # TODO: implement this
    print('TODO: print some output')

def task_3(parser):
    """Construct and output an equivalent DFA.
    The input is guaranteed to be an Epsilon Free NFA."""
    efnfa = parser.parse_fa()
    # TODO: implement this
    print('TODO: print some output')

def task_4(parser):
    """For each string, output 1 if the DFA accepts it, 0 otherwise.
    The input is guaranteed to be a DFA."""
    dfa = parser.parse_fa()
    test_strings = parser.parse_test_strings()
    # TODO: implement this
    print('TODO: print some output')

if __name__ == '__main__':

    parser = Parser()
    command = parser.parse_command()

    if command == 'epsilon-closure':
        task_1(parser)
    elif command == 'nfa-to-efnfa':
        task_2(parser)
    elif command == 'efnfa-to-dfa':
        task_3(parser)
    elif command == 'compute-dfa':
        task_4(parser)
    else:
        print(f'Command {repr(command)} not recognised.')


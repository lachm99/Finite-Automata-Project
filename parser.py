""" This module contains a very simple parser to help you read the input files.
You don't need to edit this file, but you can if you want. You can even delete
it, if you'd prefer to write your own parsing functions."""

import re
from sys import stdin

# Local custom file to represent Finite Automata
from fa import *

class Parser:
    """Combined parser and reader, takes a stream as input, outputs automata/commands"""

    def __init__(self, stream=stdin):
        """Defaults to reading from sys.stdin"""
        self.stream = stream

    def parse_command(self):
        """Grab the next line from the stream."""
        return next(self.stream).strip()

    def read_section(self):
        """Collect lines from the stream until 'end' is read."""
        lines = []
        line = next(self.stream)
        line = re.sub('\s', '', line)
        while line != 'end':
            # remove all whitespace characters
            lines.append(line)
            line = next(self.stream)
            line = re.sub('\s', '', line)
        return lines

    def parse_fa(self):
        """
        Parses a FA, creating an FA object using the custom module
        found in fa.py """
        lines = self.read_section()
        it = iter(lines)
        automata = FA()
        automata.gen_FA(it)
        return automata

    def parse_closures(self):
        """Read from the stream, return a dictionary where the keys are state
        names, and the values are lists of states reachable from the key, using
        0 or more epsilon transitions."""
        closures = dict()
        for line in self.read_section():
            state, closure = line.split(':')
            closures[state] = closure.split(',')
        return closures

    def parse_test_strings(self):
        """Read from the stream, return a list of strings (to be tested)"""
        return self.read_section()


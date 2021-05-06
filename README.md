# Finite-Automata Project
This project is built effectively to solve the string membership problem when given an NFA as input.
To do this, there are several intermediate steps which are also accessible and useful in isolation.

1. Compute the epsilon closure E(q) for each state q ∈ Q of a given NFA.
2. Use a set of epilson closures to construct an equivalent epsilon-free NFA.
3. Use an epsilon-free NFA to construct an equivalent DFA.
4. Determine if a set of input strings are recognised by a given DFA.

There is also a useful OOP abstraction of different Finite Automata which holds utility apart from this project.

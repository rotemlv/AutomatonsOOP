# an automaton has a language, states, start state, function, accepting states
from collections.abc import Iterable, Sized


class Automaton:
    def __init__(self, language: Sized and Iterable,
                 states: Sized and Iterable, start_state,
                 delta: dict, accepting_states):
        # check accepting states
        if not isinstance(accepting_states, Iterable):
            accepting_states = {accepting_states, }

        assert (state in states for state in accepting_states)

        # check start state
        assert start_state in states
        # check delta function
        assert ((u in states) and (v in language) for u, v in delta.keys())
        assert (v in states for v in delta.values())

        self.accepting_states = accepting_states
        self.delta = delta
        self.start_state = start_state
        self.states = states
        self.language = language

    """Basic string format for automaton"""
    def __str__(self):
        return f"Automaton({self.language=}, {self.states=}, {self.start_state=}, " \
            f"{self.delta=}, {self.accepting_states=})"

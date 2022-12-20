# NFA is an automaton, here we can have epsilon moves,
# and stuck-words
import copy
from collections.abc import Iterable
from typing import Sized

from PackageForAutomatons.Automaton import Automaton


class NFA(Automaton):
    """For epsilon-passes, use None as the letter in delta"""
    def __init__(self, language: Iterable, states: Iterable,
                 start_state, delta: dict, accepting_states: Iterable):
        # verify letters in delta are in the language
        for tpl in delta.keys():
            _, letter = tpl  # (state, letter)
            assert letter in language or letter is None
        # if delta points to a single state, change it to a single set!
        for u, v in delta.keys():
            if not isinstance(delta[u, v], Iterable):
                delta[u, v] = {delta[u, v]}

        super().__init__(language, states, start_state, delta, accepting_states)

    def check_if_nfa_accepts_word(self, word: Iterable and Sized, initial_state=None):
        """Returns True iff the given word has been accepted by the NDFA.
        In practice: traverses ALL possible paths over the NDFA.
        This is expensive as duck, as in 2^n expensive (worst case)"""
        assert all(letter in self.language for letter in word)
        if initial_state is None:
            initial_state = self.start_state
        regular_state = initial_state
        consumable_word = copy.copy(word)
        is_stuck = False

        while len(consumable_word):
            # check for epsilon-passes:
            epsilon_closure = {regular_state}
            for tpl in self.delta.keys():
                if (regular_state, None) == tpl:
                    # add the set of new reachable states to closure
                    epsilon_closure = epsilon_closure.\
                        union(set(self.delta[(regular_state, None)]))
            # for every state we can reach BEFORE reading a letter, do:
            for state in epsilon_closure:
                # read a letter:
                # splitting string definitely won't matter in the grand scheme of things
                t = consumable_word[0]
                consumable_word = consumable_word[1:]
                possible_states = self.delta.get((state, t))
                if possible_states is None:
                    is_stuck = True
                    break
                if isinstance(possible_states, Iterable):
                    # traverse ALL paths from current regular_state given some letter

                    return any(self.check_if_nfa_accepts_word(consumable_word, s)
                               for s in possible_states)
                else:
                    raise Exception("Delta should be a map of the form"
                                    " (regular_state, letter) -> <list of states>")
        if is_stuck:
            return False
        return regular_state in self.accepting_states

    def __str__(self):
        return f"Language: {self.language}, States: {self.states}, " \
               f"Start state: {self.start_state}, Delta: {self.delta}, " \
               f"Final state(s): {self.accepting_states}"
# DFA is an automaton, with delta that defines every single letter
from collections.abc import Iterable
from random import randint

from PackageForAutomatons.Automaton import Automaton


class DFA(Automaton):
    def __init__(self, language: Iterable, states: Iterable,
                 start_state, delta: dict, accepting_states):
        # check that our definition is valid for DFA
        for letter in language:
            for state in states:
                assert delta.get((state, letter)) is not None
        super().__init__(language, states, start_state, delta, accepting_states)

    """Traverse the word in the automaton"""
    def traverse(self, word: Iterable):
        # verify the word is defined over the alphabet of the DFA
        assert (letter in self.language for letter in word)
        # start_state
        current_state = self.start_state
        for letter in word:
            current_state = self.delta[(current_state, letter)]
        return current_state

    """Check if a word is accepted"""
    def check_word_acceptance(self, word: Iterable):
        return self.traverse(word) in self.accepting_states

    """Check for a group of words which is accepted"""
    def check_acceptance_for_words(self, words: Iterable[Iterable]):
        for word in words:
            yield word, self.traverse(word) in self.accepting_states


def main():
    dfa = DFA({'a'}, {0,1}, 0, {(0,'a'):1, (1,'a'):0}, 1)
    print(dfa)
    randwords = set()
    for _ in range(10):
        randwords.add(''.join(['a' for _ in range(randint(1,10))]))
    for w, b in dfa.check_acceptance_for_words(randwords):

        print(w, b)

if __name__ == '__main__':
    main()
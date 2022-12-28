"""TODO:
    Work in progress"""

from collections.abc import Sized, Iterable, Hashable
from collections import deque
import random

VERBOSE_PRINTS = 1


def debug_print(*args):
    if VERBOSE_PRINTS:
        print(*args)


class PDA:
    language: Sized and Iterable
    states: Sized and Iterable
    start_state: Hashable
    delta: dict
    stack_letters: Sized and Iterable
    z0: Hashable

    top_of_stack: Hashable or None
    stack: deque
    input: Sized and Iterable
    is_active: bool
    current_state: Hashable
    input_index: int
    is_stuck: bool

    def __init__(self, language: Sized and Iterable, states: Sized and Iterable,
                 start_state: Hashable, delta: dict,
                 stack_letters: Sized and Iterable, z0: Hashable):
        self.language = language
        self.states = states
        assert start_state in states
        self.start_state = start_state
        self.delta = delta
        self.stack_letters = stack_letters
        assert z0 in stack_letters
        self.z0 = z0

        self.is_active = False

    def begin_automaton_run(self, input: Sized and Iterable):
        """Prepares the PDA to run over the given input"""
        self.is_active = True
        self.is_stuck = False
        self.stack = deque([self.z0])
        self.top_of_stack = self.stack[-1]
        assert (letter in self.language for letter in input)
        # insert input
        self.input = input
        self.current_state = self.start_state
        self.input_index = 0

    def pushdown_automaton_iteration(self):
        assert self.is_active
        # read letter from input
        if self.input_index >= len(self.input):
            letter = None
        else:
            letter = self.input[self.input_index]

        # create a dict with all possible paths from our current state and magazine letter
        possible_paths = {(self.current_state, letter, self.top_of_stack),
                          (self.current_state, None, self.top_of_stack)}
        # remove non-valid paths
        possible_paths = {path for path in possible_paths if self.delta.get(path) is not None}
        # check if any paths exist
        if len(possible_paths) == 0:
            self.is_stuck = True
            debug_print(f"Stuck at {self.current_state=}, {letter=}, {self.stack=} ({self.top_of_stack=})")
            return

        # next step: choose a random way to advance
        _, actual_letter, _ = nxt = random.sample(list(possible_paths), 1)[0]
        debug_print(f"Moving from: {nxt} (state, letter, stack_top)")

        # check if there is more than one option to move towards
        if isinstance(self.delta[nxt], tuple):
            new_state, new_top = self.delta[nxt]
        else:
            assert isinstance(self.delta[nxt], Iterable and Sized)
            # pick random option if necessary
            new_state, new_top = random.sample(list(self.delta[nxt]), 1)[0]

        # log move:
        debug_print(f"Moving to: {new_state}, replacing top from {self.top_of_stack} to {new_top}")

        # increment self.input_index (if required, as in, if we actually read a letter in the chosen delta)
        if actual_letter == letter and letter is not None:
            self.input_index += 1

        # change the state
        self.current_state = new_state
        # remove the old top of the stack
        self.stack.pop()
        # add the new top to the stack (from right to left - bottom to top)
        # assuming one can add more than one symbol to the stack at the same iteration
        # configuration example: (q0, 'a', Z0) |- (q0, AAZ0), (where Z0 is the stack's first letter)
        if new_top is not None:
            for m_letter in new_top[-1::-1]:
                self.stack.append(m_letter)

        # update top of stack
        if len(self.stack) > 0:
            self.top_of_stack = self.stack[-1]
        else:
            self.top_of_stack = None

    def read_word(self, word):
        self.begin_automaton_run(word)
        while len(self.stack) and not self.is_stuck:
            self.pushdown_automaton_iteration()
            debug_print(f"Current stack {self.stack}\n")
            if self.top_of_stack is None and self.input_index < len(word):
                self.is_stuck = True
                break
        debug_print(self.input_index, len(word))
        if self.input_index == len(word) and not self.is_stuck:
            debug_print(f"Finished reading {word}, stack: {self.stack}")
            if len(self.stack) == 0:
                debug_print(f"PDA accepts the word {word}")
        else:
            debug_print(f"Failed reading {word=}, traversed part: {word[:self.input_index]}, and got stuck. "
                        f"stack: {self.stack}")

        # returns True iff word was accepted by PDA
        return self.input_index == len(word) and not self.is_stuck


def main():
    # This example uses a string as the stack, and hence limits the character-length
    # of any letter in the stack to 1, but one could easily change this
    # to be a list (no need to change the code)

    # dct = {(0, None, 'x'): (0, None),
    #        (0, 'b', 'x'): (0, 'x'),
    #        (0, 'a', 'x'): (1, 'xx'),
    #        (0, 'a', 'w'): (1, 'x'),
    #        (1, None, 'x'): (0, 'x'),
    #        (1, 'a', 'x'): {(1, 'xx'), (0, 'xx')}}

    # example for using a list-stack
    # (this example is incomplete but will work on some inputs)
    dct = {
        (0, 'a', 'z0'): (0, ['A', 'z0']),
        (0, 'b', 'z0'): (0, ['B', 'z0']),

        (0, 'a', 'A'): (0, ['A', 'A']),
        (0, 'b', 'B'): (0, ['B', 'B']),

        (0, 'a', 'B'): (0, None),
        (0, 'b', 'A'): (0, None),
        (0, None, 'z0'): (0, None)

    }

    pda = PDA({'a', 'b'}, [0], 0, dct, {'z0', 'A', 'B'}, 'z0')
    # pda.begin_automaton_run("aa")
    # pda.pushdown_automaton_iteration()
    # pda.pushdown_automaton_iteration()
    # debug_debug_print(pda.stack)
    pda.read_word("bbbaaaa")

    #  pda.pushdown_automaton_iteration()
    # x = dct[1,'a','x']
    # debug_print(x)
    # debug_print(random.sample(list(x), 1))
    # tmp = {(1, 2), (2, 3)}
    # for _ in range(5):
    #     debug_print(tmp, random.sample(list(tmp), 1))


if __name__ == '__main__':
    main()

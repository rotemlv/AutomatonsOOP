from Direction import *

BLANKS_TO_APPEND = 50


class TuringMachine:
    tape: list or None

    def __init__(self, alphabet, states, start_state,
                 acc, rej, delta, tape_alphabet, blank):
        self.alphabet = alphabet
        self.states = states
        self.start_state = start_state
        self.acc = acc
        self.rej = rej
        self.delta = delta
        self.tape_alphabet = tape_alphabet
        self.blank = blank
        self.tape_in = False
        self.verbose = False

    def __str__(self):
        return f"{self.alphabet=}, {self.states}, {self.start_state}," \
               f" {self.acc}, {self.rej}, {self.delta}," \
               f" {self.tape_alphabet}, {self.blank}"

    def place_tape(self, tape: list):
        self.tape = tape
        self.tape_in = True

    """Removes *and returns* the current tape"""
    def remove_tape(self):
        output, self.tape = self.tape, None
        self.tape_in = False
        return output

    def set_verbose_output(self, boolean: bool):
        self.verbose = boolean

    def move_head(self, old_head_position: int, direction: Direction):
        if self.tape_in:
            # edge cases
            if old_head_position == 0 and direction == Direction.LEFT:
                # stay
                return old_head_position
            if old_head_position == len(self.tape) - 1 and direction == Direction.RIGHT:
                # pump with blanks
                self.tape = self.tape + [b] * BLANKS_TO_APPEND
                # and allow movement
                return 1 + old_head_position

            # regular cases
            if direction == Direction.RIGHT:
                return old_head_position + 1
            if direction == Direction.LEFT:
                return old_head_position - 1
            if direction == Direction.STAY:
                return old_head_position
        else:
            raise Exception("Turing machine failed to read (no tape).")

    def traverse_contained_tape(self):
        # set header to the first element in the tape:
        head = 0
        state = self.start_state
        # while
        while state not in {self.acc, self.rej}:
            if self.verbose:
                print(f"Reading: {head = }, head ->"
                      f" {self.tape[head]}, {state = }")
            # perform op
            new_state, new_letter, direction = self.turing_iteration(state, head)
            if self.verbose:
                print(f"Changing to: {new_state = },"
                      f" {new_letter = }, {direction = }\n")
            # replace tape letter with l
            self.tape[head] = new_letter
            # move header
            head = self.move_head(head, direction)
            # change state
            state = new_state
        return state == self.acc

    def traverse_tape(self, tape: list):
        self.place_tape(tape)
        ret = self.traverse_contained_tape()
        self.remove_tape()
        return ret

    def turing_iteration(self, state, head):
        # get letter at head
        letter = self.tape[head]
        # use delta
        s, l, d = self.delta[state, letter]
        # should really be LSD
        return s, l, d


if __name__ == '__main__':
    # the basic example I saw when I first learned about these
    S = Direction.STAY
    L = Direction.LEFT
    R = Direction.RIGHT
    lang = {'a', 'b'}
    states = {0, 1, 2, 3, 4, 5}
    rej = 4
    acc = 5
    start = 0
    b = ' '
    tape_lang = {'a', 'b', b, 'a*', 'b*'}
    delta = {
        (0, b): (acc, b, S),
        (0, 'a'): (1, 'a*', R),
        (0, 'b'): (rej, b, S),
        (0, 'b*'): (3, 'b*', R),  # verify we marked all b's

        (1, 'a'): (1, 'a', R),
        (1, 'b*'): (1, 'b*', R),
        (1, 'b'): (2, 'b*', L),
        (1, b): (rej, b, S),

        (2, 'b*'): (2, 'b*', L),
        (2, 'a'): (2, 'a', L),
        (2, 'a*'): (0, 'a*', R),

        (3, 'b'): (rej, 'b', S),
        (3, 'b*'): (3, 'b*', R),
        (3, b): (acc, b, S),

    }

    m = TuringMachine(lang, states, start, acc, rej, delta, tape_lang, b)
    word = 'aaabb'
    x = m.traverse_tape([*word])
    print(x)
